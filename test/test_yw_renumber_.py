""" Python unit tests for the yw_renumber project.

Test suite for yw_renumber.pyw.

For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from shutil import copyfile
import os
import unittest
import yw_renumber_


# Test environment

# The paths are relative to the "test" directory,
# where this script is placed and executed

TEST_PATH = os.getcwd() + '/../test'
TEST_DATA_PATH = TEST_PATH + '/data/'
TEST_EXEC_PATH = TEST_PATH + '/yw7/'

# To be placed in TEST_DATA_PATH:
NORMAL_YW7 = TEST_DATA_PATH + 'normal.yw7'
NORMAL_HTML = TEST_DATA_PATH + 'normal.html'
NORMAL_CSV = TEST_DATA_PATH + 'normal.csv'
INI_HTML = TEST_DATA_PATH + 'html.ini'
INI_CSV = TEST_DATA_PATH + 'csv.ini'

# Test data
TEST_YW7 = TEST_EXEC_PATH + 'yw7 Sample Project.yw7'
TEST_HTML = TEST_EXEC_PATH + 'yw7 Sample Project_report.html'
TEST_CSV = TEST_EXEC_PATH + 'yw7 Sample Project_report.csv'
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
        os.remove(TEST_HTML)
    except:
        pass

    try:
        os.remove(TEST_EXEC_PATH + INI_FILE)
    except:
        pass

    try:
        os.remove(TEST_CSV)
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
        self.assertEqual(read_file(TEST_HTML), read_file(NORMAL_HTML))

    def test_html(self):
        copyfile(NORMAL_YW7, TEST_YW7)
        copyfile(INI_HTML, TEST_INI)
        os.chdir(TEST_EXEC_PATH)
        yw_renumber_.run(TEST_YW7, silentMode=True)
        self.assertEqual(read_file(TEST_HTML), read_file(NORMAL_HTML))

    def test_csv(self):
        copyfile(NORMAL_YW7, TEST_YW7)
        copyfile(INI_CSV, TEST_INI)
        os.chdir(TEST_EXEC_PATH)
        yw_renumber_.run(TEST_YW7, silentMode=True, installDir=TEST_EXEC_PATH)
        self.assertEqual(read_file(TEST_CSV), read_file(NORMAL_CSV))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
