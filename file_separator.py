from dataclasses import dataclass
from typing import List
from enum import Enum


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
        pass

    @classmethod
    def preview(cls, fso: FileSeparatorOptions):
        pass
