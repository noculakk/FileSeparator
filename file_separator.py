import time
import os
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class DateDirFormat(Enum):
    dmy = 1
    my = 2
    y = 3


@dataclass
class FileSeparatorOptions:
    base_dir: str
    target_dir: str
    extensions: List[str]
    by_date_order: DateDirFormat
    by_size_order: List[int]
    make_empty_dir: bool
    remove_org_files: bool


class FileSeparator:

    @classmethod
    def run(cls, fso: FileSeparatorOptions):
        if not os.path.isdir(fso.base_dir) or not os.path.isdir(fso.target_dir):
            raise ValueError('directory does not exist')

        if fso.base_dir == fso.target_dir:
            raise ValueError('base and target directory cannot be the same')

        if not fso.extensions == []:
            files = [f for f in cls.get_all_files(fso.base_dir) if os.path.splitext(f[0])[1] in fso.extensions]
        else:
            files = cls.get_all_files(fso.base_dir)



    @classmethod
    def preview(cls, fso: FileSeparatorOptions):
        pass

    @classmethod
    def get_all_files(cls, root_dir: str) -> List[Tuple[str, datetime, int]]:
        """
        :return: list of files with paths relative to root_dir, creation dates, sizes
        """
        files_list = []

        for dir_path, _, files in os.walk(root_dir):
            for f in files:
                f_path = os.path.join(dir_path, f)
                f_size = os.path.getsize(f_path)

                f_time = time.ctime(os.path.getctime(f_path))
                f_date = datetime.strptime(f_time, '%a %b %d %H:%M:%S %Y')

                files_list.append((f_path, f_date, f_size))

        return files_list

    @classmethod
    def separate_by_size(cls, files: List[Tuple[str, datetime, int]], separators_list: List[int]):
        if len(separators_list) == 1:
            return { (-1, -1): files}

        dictionary = { (-1, separators_list[0]): [], (separators_list[-1], -1): []}

        for i in range(1, len(dictionary) - 1):
            dictionary[(separators_list[i - 1], separators_list[i])] = []

        for f in files:
            for key in dictionary.keys():
                if key[0] < f[2] <= key[1] or (key[1] == -1 and f[2] > key[0]):
                    dictionary[key].append(f)

        return dictionary

    @classmethod
    def separate_by_date(cls, files: List[Tuple[str, datetime, int]], date_format: DateDirFormat):
        date_list = [date for _, date, _ in files]
        oldest = min(date_list)
        youngest = max(date_list)
        delta_time = relativedelta(oldest, youngest)

        dictionary = {}
        if date_format == DateDirFormat.dmy:
            for d in range(delta_time.days + 1):
                day = oldest + relativedelta(days=d)
                dictionary[day] = []

            for f in files:
                for key in dictionary.keys():
                    if key.year == f[1].year and key.month == f[1].month and key.day == f[1].day:
                        dictionary[key].append(f)

            return dictionary

        if date_format == DateDirFormat.my:
            for m in range(delta_time.months + 1):
                month = oldest + relativedelta(months=m)
                dictionary[month] = []
            for f in files:
                for key in dictionary.keys():
                    if key.year == f[1].year and key.month == f[1].month:
                        dictionary[key].append(f)

            return dictionary

        for y in range(delta_time.years +1):
            year = oldest + relativedelta(years=y)
            dictionary[year] = []

            for f in files:
                for key in dictionary.keys():
                    if key.year == f[1].year:
                        dictionary[key].append(f)

        return dictionary