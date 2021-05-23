from unittest import TestCase
from datetime import datetime

from src.file_separator import DateDirFormat
from src.parser import Parser


class TestParser(TestCase):
    def test_date_to_str(self):
        self.assertEqual('2020-07-20', Parser.date_to_str(datetime(year=2020, month=7, day=20), DateDirFormat.dmy))
        self.assertEqual('2017-04', Parser.date_to_str(datetime(year=2017, month=4, day=1), DateDirFormat.my))
        self.assertEqual('2020', Parser.date_to_str(datetime(year=2020, month=1, day=1), DateDirFormat.y))

    def test_sizes_to_int(self):
        self.assertEqual([1024], Parser.sizes_to_int('1 KB'))
        self.assertEqual([512], Parser.sizes_to_int('512 B'))
        self.assertEqual([1024, 1024 ** 3], Parser.sizes_to_int('1 GB, 1 KB'))

    def test_int_to_str(self):
        self.assertEqual('1.00 KB - 1.00 GB', Parser.int_to_str((1024, 1024 ** 3)))
        self.assertEqual('> 2.50 KB', Parser.int_to_str((2560, -1)))
        self.assertEqual('< 5.00 MB', Parser.int_to_str((-1, 5 * 1024 ** 2)))
        self.assertEqual('Wszystkie pliki', Parser.int_to_str((-1, -1)))
