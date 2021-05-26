import time
import os
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from shutil import copy2
from calendar import monthrange
from src.tools import is_dictionary_empty, flatten_dict
from file_separator_error import *


class DateDirFormat(Enum):
    dmy = 0
    my = 1
    y = 2


@dataclass
class FileSeparatorOptions:
    base_dir: str
    target_dir: str
    extensions: List[str]
    by_date_order: DateDirFormat
    by_creation_date: bool
    by_size_order: List[int]
    make_empty_dir: bool
    remove_org_files: bool


class Parser:
    @classmethod
    def extensions_to_list(cls, extensions: str) -> List[str]:
        if extensions == '':
            return []
        extensions_list = [ext.strip() for ext in extensions.split(',')]
        if not all(len(e.split()) == 1 and e[0] == '.' for e in extensions_list):
            raise ValueError("Rozszerzenie podane w blednej formie")
        return extensions_list

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
            raise DirectoryNotExistError()

        if not fso.extensions == []:
            files = [f for f in cls.get_all_files(fso.base_dir, fso.by_creation_date) if os.path.splitext(f[0])[1] in fso.extensions]
        else:
            files = cls.get_all_files(fso.base_dir, fso.by_creation_date)

        if not files:
            raise EmptyFilesListError()

        if fso.by_size_order is not None:
            cls.run_by_size(files, fso)

        elif fso.by_date_order is not None:
            cls.run_by_date(files, fso)

        else:
            raise NotImplementedError()

    @classmethod
    def run_by_date(cls, files, fso):
        dictionary = cls.separate_by_date(files, fso.by_date_order)
        flat_dictionary = flatten_dict(dictionary)

        for path, files in flat_dictionary.items():
            if not fso.make_empty_dir and not flat_dictionary[path]:
                continue

            path = os.path.join(fso.target_dir, path)

            if os.path.isdir(path):
                path = path + '___FileSeparator'

            os.makedirs(path)

            for f in files:
                copy2(f[0], path)

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
    def get_all_files(cls, root_dir: str, by_creation_date) -> List[Tuple[str, datetime, int]]:
        """
        :return: list of files with paths relative to root_dir, creation dates, sizes
        """
        files_list = []

        for dir_path, _, files in os.walk(root_dir):
            for f in files:
                f_path = os.path.join(dir_path, f)
                f_size = os.path.getsize(f_path)

                f_time = time.ctime(os.path.getctime(f_path) if by_creation_date else os.path.getmtime(f_path))
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
            dictionary[(year.year, )] = []

            for f in files:
                for key in dictionary.keys():
                    if key[0] == f[1].year:
                        dictionary[key].append(f)

        if date_format == DateDirFormat.my or date_format == DateDirFormat.dmy:
            for k, v in dictionary.items():
                dictionary[k] = {}

                for m in range(1, 13):
                    month = datetime(year=k[0], month=m, day=1)
                    dictionary[k][(k[0], month.month)] = []

                for f in v:
                    for key in dictionary[k].keys():
                        if key[0] == f[1].year and key[1] == f[1].month:
                            dictionary[k][key].append(f)

        if date_format == DateDirFormat.dmy:
            for k_1, v_1 in dictionary.items():
                for k_2, v_2 in dictionary[k_1].items():
                    dictionary[k_1][k_2] = {}

                    for d in range(monthrange(k_2[0], k_2[1])[1]):
                        day = datetime(year=k_2[0], month=k_2[1], day=d + 1)
                        dictionary[k_1][k_2][(k_2[0], k_2[1], day.day)] = []

                    for f in v_2:
                        for key in dictionary[k_1][k_2].keys():
                            if key[0] == f[1].year and key[1] == f[1].month and key[2] == f[1].day:
                                dictionary[k_1][k_2][key].append(f)

        return dictionary


# Test
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
