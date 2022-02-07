#!/usr/bin/env python3
"""Renumber yWriter chapters. 

Version @release
Requires Python 3.6+
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import argparse
from pathlib import Path

from pywriter.config.configuration import Configuration
from pywriter.ui.ui import Ui

from ywrenumber.yw_rn import YwRn
from ywrenumber.yw_renumber_tk import YwRenumberTk


SUFFIX = '_report'
APPNAME = 'yw-renumber'

SETTINGS = dict(
    yw_last_open='',
    numbering_style='0',
    numbering_case='0',
    heading_prefix='||',
    heading_suffix='||',
)

OPTIONS = dict(
    ren_unused=False,
    ren_parts=False,
)


def run(sourcePath, silentMode=True, installDir=''):

    #--- Load configuration

    sourceDir = os.path.dirname(sourcePath)

    if not sourceDir:
        sourceDir = './'

    else:
        sourceDir += '/'

    iniFile = f'{installDir}{APPNAME}.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = dict(
        suffix=SUFFIX,
    )
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    converter = YwRn()

    if silentMode:
        converter.ui = Ui('')
        converter.run(sourcePath, **kwargs)

    else:
        converter.ui = YwRenumberTk('Renumber yWriter chapters @release', **kwargs)
        converter.ui.converter = converter

        #--- Get initial project path.

        if not sourcePath or not os.path.isfile(sourcePath):
            sourcePath = kwargs['yw_last_open']

        #--- Instantiate the viewer object.

        converter.ui.open_project(sourcePath)
        converter.ui.start()

        #--- Save project specific configuration

        for keyword in converter.ui.kwargs:

            if keyword in configuration.options:
                configuration.options[keyword] = converter.ui.kwargs[keyword]

            elif keyword in configuration.settings:
                configuration.settings[keyword] = converter.ui.kwargs[keyword]

            configuration.write(iniFile)


if __name__ == '__main__':

    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}/config/'

    except:
        installDir = ''

    os.makedirs(installDir, exist_ok=True)

    if len(sys.argv) == 1:
        run('', False, installDir)

    else:
        parser = argparse.ArgumentParser(
            description='Renumber yWriter chapters',
            epilog='')
        parser.add_argument('sourcePath',
                            metavar='Sourcefile',
                            help='The path of the yWriter project file.')

        parser.add_argument('--silent',
                            action="store_true",
                            help='operation without grphical user interface; suppress error messages')
        args = parser.parse_args()
        run(args.sourcePath, args.silent, installDir)
