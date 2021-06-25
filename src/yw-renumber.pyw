#!/usr/bin/env python3
"""Configurable reports from yWriter. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from configparser import ConfigParser

from ywrenumber.yw_rn import YwRn
from ywrenumber.rn_ui import RnUi


def run(sourcePath):

    #--- Try to get persistent configuration data

    iniPath = os.getenv('APPDATA').replace('\\', '/') + '/yw-renumber'

    if not os.path.isdir(iniPath):
        os.makedirs(iniPath)

    iniFile = iniPath + '/yw-renumber.ini'
    config = ConfigParser()

    options = []

    try:
        config.read(iniFile)

        if sourcePath is None:
            sourcePath = config.get('FILES', 'yw_last_open')

            if sourcePath == 'None':
                sourcePath = None

        for i in range(RnUi.optionsTotal):
            options.append(config.get('OPTIONS', str(i)))

    except:

        for i in range(RnUi.optionsTotal):
            options.append(False)

        # Fix preset.

        options[2] = 0
        options[3] = 0
        options[4] = ''
        options[5] = ''

    #--- Instantiate a user interface object

    ui = RnUi('Renumber yWriter chapters @release')

    optionCnt = 0
    ui.Parts.set(options[optionCnt])
    optionCnt += 1
    ui.Unused.set(options[optionCnt])
    optionCnt += 1
    ui.Style.set(options[optionCnt])
    optionCnt += 1
    ui.Case.set(options[optionCnt])
    optionCnt += 1
    ui.Prefix.set(options[optionCnt].replace('|', ''))
    optionCnt += 1
    ui.Suffix.set(options[optionCnt].replace('|', ''))

    if sourcePath is not None:

        if os.path.isfile(sourcePath):
            ui.sourcePath = sourcePath
            ui.set_info_what(
                'File: ' + os.path.normpath(sourcePath))
            ui.root.runButton.config(state='normal')

        else:
            sourcePath = None

    converter = YwRn()
    # instantiate a converter object

    # Create a bidirectional association between the
    # user interface object and the converter object.

    converter.ui = ui
    # make the user interface's methods visible to the converter

    ui.converter = converter
    # make the converter's methods visible to the user interface

    ui.start()

    #--- Save configuration

    if ui.sourcePath is not None:
        sourcePath = ui.sourcePath

    else:
        sourcePath = 'None'

    if not config.has_section('FILES'):
        config.add_section('FILES')

    config.set('FILES', 'yw_last_open', sourcePath)

    if not config.has_section('OPTIONS'):
        config.add_section('OPTIONS')

    optionCnt = 0
    config.set('OPTIONS', str(optionCnt), str(ui.Parts.get()))
    optionCnt += 1
    config.set('OPTIONS', str(optionCnt), str(ui.Unused.get()))
    optionCnt += 1
    config.set('OPTIONS', str(optionCnt), str(ui.Style.get()))
    optionCnt += 1
    config.set('OPTIONS', str(optionCnt), str(ui.Case.get()))
    optionCnt += 1
    config.set('OPTIONS', str(optionCnt), '|' + str(ui.Prefix.get() + '|'))
    optionCnt += 1
    config.set('OPTIONS', str(optionCnt), '|' + str(ui.Suffix.get() + '|'))

    with open(iniFile, 'w') as f:
        config.write(f)


if __name__ == '__main__':

    try:
        sourcePath = sys.argv[1].replace('\\', '/')

    except:
        sourcePath = None

    run(sourcePath)
