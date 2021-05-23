from src.file_separator import DateDirFormat
from datetime import datetime
from typing import List, Tuple


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
        units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}

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
            return f'< {"%.2f" % end[0]} {end[1]}'

        if size[0] != -1 and size[1] == -1:
            return f'> {"%.2f" % start[0]} {start[1]}'

        if size[0] == -1 and size[1] == -1:
            return 'Wszystkie pliki'
