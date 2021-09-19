#!/usr/bin/env python3
"""Configurable reports from yWriter. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import argparse
from pywriter.config.configuration import Configuration

from pywriter.ui.ui import Ui

from ywrenumber.yw_rn import YwRn
from ywrenumber.rn_ui import RnUi


SUFFIX = '_report'
APPNAME = 'yw-renumber'

SETTINGS = dict(
    yw_last_open='',
    numberingStyle='0',
    numberingCase='0',
    headingPrefix='||',
    headingSuffix='||',
)

OPTIONS = dict(
    ren_unused=False,
    ren_parts=False,
)


def run(sourcePath, silentMode=True, installDir=''):

    #--- Load configuration

    sourceDir = os.path.dirname(sourcePath)

    if sourceDir == '':
        sourceDir = './'

    else:
        sourceDir += '/'

    iniFile = installDir + APPNAME + '.ini'
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
        converter.ui = RnUi('Renumber yWriter chapters @release', sourcePath=sourcePath, **kwargs)
        converter.ui.converter = converter
        converter.ui.start()

        #--- Save project specific configuration

        for keyword in converter.ui.kwargs:

            if keyword in configuration.options:
                configuration.options[keyword] = converter.ui.kwargs[keyword]

            elif keyword in configuration.settings:
                configuration.settings[keyword] = converter.ui.kwargs[keyword]

            configuration.write(iniFile)


if __name__ == '__main__':
    installDir = os.getenv('APPDATA').replace('\\', '/') + '/pyWriter/' + APPNAME + '/config/'
    os.makedirs(installDir, exist_ok=True)

    if len(sys.argv) == 1:
        run('', False, installDir)

    else:
        parser = argparse.ArgumentParser(
            description='yWriter report generator',
            epilog='')
        parser.add_argument('sourcePath',
                            metavar='Sourcefile',
                            help='The path of the yWriter project file.')

        parser.add_argument('--silent',
                            action="store_true",
                            help='suppress error messages and the request to confirm overwriting')
        args = parser.parse_args()
        run(args.sourcePath, args.silent, installDir)
