"""Build a Python script for the yw-renumber distribution.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the pywriter package.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}yw_renumber_.pyw'
TARGET_FILE = f'{BUILD}yw_renumber.pyw'


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'ywrenumberlib', '../src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'pywriter', '../src/')
    # inliner.run(SOURCE_FILE, TARGET_FILE, 'ywrenumberlib', '../src/', copyPyWriter=True)
    # inliner.run(TARGET_FILE, TARGET_FILE, 'pywriter', '../../PyWriter/src/', copyPyWriter=True)
    print('Done.')


if __name__ == '__main__':
    main()
