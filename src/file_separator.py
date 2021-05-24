import time
import os
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from shutil import copy2
from calendar import monthrange
from src.tools import is_dictionary_empty


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


class Parser:
    @classmethod
    def date_to_str(cls, dt: datetime, format: DateDirFormat) -> str:
        if format is DateDirFormat.dmy:
            return dt.strftime('%Y-%m-%d')

        if format is DateDirFormat.my:
            return dt.strftime('%Y-%m')

        return dt.strftime('%Y')

    @classmethod
    def sizes_to_int(cls, sizes_str: str) -> List[int]:
        units = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3}

        sizes = sizes_str.split(',')
        sizes = [el.strip() for el in sizes]
        sizes = [tuple(el.split()) for el in sizes]

        for i in range(len(sizes)):
            if len(sizes[i]) != 2:
                raise ValueError('Tuple has not 2 elements!')
            if sizes[i][1] not in units:
                raise ValueError('Invalid unit!')

            if not sizes[i][0].isnumeric():
                raise ValueError('Size is not a number!')

        return list(sorted([int(s[0]) * units[s[1]] for s in sizes]))

    @classmethod
    def int_to_str(cls, size: Tuple[int, int]) -> str:
        units = ['B', 'KB', 'MB', 'GB']
        start = [size[0], units[0]]
        end = [size[1], units[0]]
        c1, c2 = 1, 1

        if size[0] != -1:
            while start[0] >= 1024:
                start[0] /= 1024
                start[1] = units[c1]
                c1 += 1

        if size[1] != -1:
            while end[0] >= 1024:
                end[0] /= 1024
                end[1] = units[c2]
                c2 += 1

        if size[0] != -1 and size[1] != -1:
            return f'{"%.2f" % start[0]} {start[1]} - {"%.2f" % end[0]} {end[1]}'

        if size[0] == -1 and size[1] != -1:
            return f'Mniejsze niż {"%.2f" % end[0]} {end[1]}'

        if size[0] != -1 and size[1] == -1:
            return f'Większe niż {"%.2f" % start[0]} {start[1]}'

        if size[0] == -1 and size[1] == -1:
            return 'Wszystkie pliki'


class FileSeparator:

    @classmethod
    def run(cls, fso: FileSeparatorOptions):
        if not os.path.isdir(fso.base_dir) or not os.path.isdir(fso.target_dir):
            raise ValueError('directory does not exist')

        if not fso.extensions == []:
            files = [f for f in cls.get_all_files(fso.base_dir) if os.path.splitext(f[0])[1] in fso.extensions]
        else:
            files = cls.get_all_files(fso.base_dir)

        if fso.by_size_order is not None:
            cls.run_by_size(files, fso)

        elif fso.by_date_order is not None:
            cls.run_by_date(files, fso)

        else:
            raise NotImplementedError()

    @classmethod
    def run_by_date(cls, files, fso):
        dictionary = cls.separate_by_date(files, fso.by_date_order)
        for year in dictionary:
            str_year = Parser.date_to_str(year, DateDirFormat.y)
            path_year = os.path.join(fso.target_dir, str_year)

            if os.path.isdir(path_year):
                path_year = path_year + '___FileSeparator'

            if not fso.make_empty_dir and is_dictionary_empty(dictionary[year]):
                continue

            os.mkdir(path_year)

            if fso.by_date_order == DateDirFormat.y:
                for f in dictionary[year]:
                    copy2(f[0], path_year)

                    if fso.remove_org_files:
                        os.remove(f[0])
                        if not os.listdir(os.path.dirname(f[0])):
                            os.rmdir(os.path.dirname(f[0]))

            elif fso.by_date_order == DateDirFormat.my or fso.by_date_order == DateDirFormat.dmy:
                for month in dictionary[year]:
                    str_month = Parser.date_to_str(month, DateDirFormat.my)
                    path_month = os.path.join(fso.target_dir, str_year, str_month)

                    if os.path.isdir(path_month):
                        path_month = path_month + '___FileSeparator'

                    if not fso.make_empty_dir and is_dictionary_empty(dictionary[year][month]):
                        continue

                    os.mkdir(path_month)

                    if fso.by_date_order == DateDirFormat.my:
                        for f in dictionary[year][month]:
                            copy2(f[0], path_month)

                            if fso.remove_org_files:
                                os.remove(f[0])
                                if not os.listdir(os.path.dirname(f[0])):
                                    os.rmdir(os.path.dirname(f[0]))

                    else:
                        for day in dictionary[year][month]:
                            str_day = Parser.date_to_str(day, DateDirFormat.dmy)
                            path_day = os.path.join(fso.target_dir, str_year, str_month, str_day)

                            if os.path.isdir(path_month):
                                path_month = path_month + '___FileSeparator'

                            if not fso.make_empty_dir and is_dictionary_empty(dictionary[year][month][day]):
                                continue

                            os.mkdir(path_day)

                            for f in dictionary[year][month][day]:
                                copy2(f[0], path_day)

                                if fso.remove_org_files:
                                    os.remove(f[0])
                                    if not os.listdir(os.path.dirname(f[0])):
                                        os.rmdir(os.path.dirname(f[0]))

    @classmethod
    def run_by_size(cls, files, fso):
        dictionary = cls.separate_by_size(files, fso.by_size_order)
        for k in dictionary:
            str_k = Parser.int_to_str(k)
            path_k = os.path.join(fso.target_dir, str_k)

            if os.path.isdir(path_k):
                path_k = path_k + '___FileSeparator'

            if not fso.make_empty_dir and is_dictionary_empty(dictionary[k]):
                continue

            os.mkdir(path_k)

            for f in dictionary[k]:
                copy2(f[0], path_k)

                if fso.remove_org_files:
                    os.remove(f[0])
                    if not os.listdir(os.path.dirname(f[0])):
                        os.rmdir(os.path.dirname(f[0]))

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

                f_time = time.ctime(os.path.getmtime(f_path))
                f_date = datetime.strptime(f_time, '%a %b %d %H:%M:%S %Y')

                files_list.append((f_path, f_date, f_size))

        return files_list

    @classmethod
    def separate_by_size(cls, files: List[Tuple[str, datetime, int]], separators_list: List[int]):
        if len(separators_list) == 0:
            return {(-1, -1): files}

        dictionary = {(-1, separators_list[0]): [], (separators_list[-1], -1): []}

        for i in range(1, len(separators_list)):
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
        delta_time = youngest.year - oldest.year

        dictionary = {}

        for y in range(delta_time + 1):
            year = oldest + relativedelta(years=y)
            dictionary[year] = []

            for f in files:
                for key in dictionary.keys():
                    if key.year == f[1].year:
                        dictionary[key].append(f)

        if date_format == DateDirFormat.my or date_format == DateDirFormat.dmy:
            for k, v in dictionary.items():
                dictionary[k] = {}

                for m in range(1, 13):
                    month = datetime(year=k.year, month=m, day=1)
                    dictionary[k][month] = []

                for f in v:
                    for key in dictionary[k].keys():
                        if key.year == f[1].year and key.month == f[1].month:
                            dictionary[k][key].append(f)

        if date_format == DateDirFormat.dmy:
            for k_1, v_1 in dictionary.items():
                for k_2, v_2 in dictionary[k_1].items():
                    dictionary[k_1][k_2] = {}

                    for d in range(monthrange(k_2.year, k_2.month)[1]):
                        day = datetime(year=k_2.year, month=k_2.month, day=d + 1)
                        dictionary[k_1][k_2][day] = []

                    for f in v_2:
                        for key in dictionary[k_1][k_2].keys():
                            if key.year == f[1].year and key.month == f[1].month and key.day == f[1].day:
                                dictionary[k_1][k_2][key].append(f)

        return dictionary


if __name__ == '__main__':
    FileSeparator.run(FileSeparatorOptions(
        base_dir='C:\\Wszystko\\Dokumenty\\Studia\\IV semestr\\J skryptowe\\Projekt_test\\Stary',
        target_dir='C:\\Wszystko\\Dokumenty\\Studia\\IV semestr\\J skryptowe\\Projekt_test\\Nowy',
        extensions=[],
        by_date_order=DateDirFormat.dmy,
        by_size_order=None,
        make_empty_dir=False,
        remove_org_files=False
    ))
