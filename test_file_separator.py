from unittest import TestCase
from file_separator import FileSeparator
import os
import shutil
import datetime


class TestFileSeparator(TestCase):
    @classmethod
    def setUp(cls) -> None:
        os.mkdir('TestDir')
        open('TestDir\\test1', 'a').close()
        open('TestDir\\test1b', 'a').close()
        open('TestDir\\test1c', 'a').close()

    @classmethod
    def tearDown(cls) -> None:
        shutil.rmtree('TestDir')

    def test_get_all_files(self):

        files = FileSeparator.get_all_files('TestDir')

        self.assertEqual(3, len(files))
        self.assertEqual('TestDir\\test1', files[0][0])
        self.assertEqual('TestDir\\test1b', files[1][0])
        self.assertEqual('TestDir\\test1c', files[2][0])

        self.assertEqual(datetime.datetime.now().strftime('%Y %m %d'), files[0][1].strftime('%Y %m %d'))
        self.assertEqual(datetime.datetime.now().strftime('%Y %m %d'), files[1][1].strftime('%Y %m %d'))
        self.assertEqual(datetime.datetime.now().strftime('%Y %m %d'), files[2][1].strftime('%Y %m %d'))
