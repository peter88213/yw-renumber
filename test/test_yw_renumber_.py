"""Regression test for the yw_renumber project.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from shutil import copyfile
import os
import unittest
import yw_renumber_

UPDATE = False

# Test environment

# The paths are relative to the "test" directory,
# where this script is placed and executed

TEST_PATH = os.getcwd() + '/../test'
TEST_DATA_PATH = TEST_PATH + '/data/'
TEST_EXEC_PATH = TEST_PATH + '/'

# To be placed in TEST_DATA_PATH:
NORMAL_YW7 = TEST_DATA_PATH + 'normal.yw7'
DEFAULT_YW7 = TEST_DATA_PATH + 'default.yw7'
ROMAN_YW7 = TEST_DATA_PATH + 'roman.yw7'
WRITTEN_YW7 = TEST_DATA_PATH + 'written.yw7'
INI_ROMAN = TEST_DATA_PATH + 'roman.ini'
INI_WRITTEN = TEST_DATA_PATH + 'written.ini'

# Test data
TEST_YW7 = TEST_EXEC_PATH + 'yw7 Sample Project.yw7'
TEST_YW7_BAK = TEST_YW7 + '.bak'
TEST_INI = TEST_EXEC_PATH + 'yw-renumber.ini'


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


def remove_all_testfiles():
    try:
        os.remove(TEST_YW7)
    except:
        pass
    try:
        os.remove(TEST_YW7_BAK)
    except:
        pass
    try:
        os.remove(TEST_INI)
    except:
        pass


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):
        try:
            os.mkdir(TEST_EXEC_PATH)
        except:
            pass
        remove_all_testfiles()

    def test_defaults(self):
        copyfile(NORMAL_YW7, TEST_YW7)
        os.chdir(TEST_EXEC_PATH)
        yw_renumber_.run(TEST_YW7, silentMode=True)
        if UPDATE:
            copyfile(TEST_YW7, DEFAULT_YW7)
        self.assertEqual(read_file(TEST_YW7), read_file(DEFAULT_YW7))
        self.assertEqual(read_file(TEST_YW7_BAK), read_file(NORMAL_YW7))

    def test_roman(self):
        copyfile(NORMAL_YW7, TEST_YW7)
        copyfile(INI_ROMAN, TEST_INI)
        os.chdir(TEST_EXEC_PATH)
        yw_renumber_.run(TEST_YW7, silentMode=True, installDir=TEST_EXEC_PATH)
        if UPDATE:
            copyfile(TEST_YW7, ROMAN_YW7)
        self.assertEqual(read_file(TEST_YW7), read_file(ROMAN_YW7))
        self.assertEqual(read_file(TEST_YW7_BAK), read_file(NORMAL_YW7))

    def test_written(self):
        copyfile(NORMAL_YW7, TEST_YW7)
        copyfile(INI_WRITTEN, TEST_INI)
        os.chdir(TEST_EXEC_PATH)
        yw_renumber_.run(TEST_YW7, silentMode=True, installDir=TEST_EXEC_PATH)
        if UPDATE:
            copyfile(TEST_YW7, WRITTEN_YW7)
        self.assertEqual(read_file(TEST_YW7), read_file(WRITTEN_YW7))
        self.assertEqual(read_file(TEST_YW7_BAK), read_file(NORMAL_YW7))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
