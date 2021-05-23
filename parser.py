from file_separator import DateDirFormat
from datetime import datetime
from typing import List, Tuple


class Parser:
    @classmethod
    def date_to_str(cls, dt: datetime, format: DateDirFormat) -> str:
        pass

    @classmethod
    def sizes_to_int(cls, sizes_str: str) -> List[int]:
        pass

    @classmethod
    def int_to_str(cls, size: Tuple[int, int]) -> str:
        pass


