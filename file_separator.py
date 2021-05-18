from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
from datetime import datetime
import os
import time


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
            raise ValueError('komunikat folder nie istnieje')

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
