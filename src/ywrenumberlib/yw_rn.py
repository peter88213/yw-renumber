"""Provide a report generator class for yWriter projects. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File


class YwRn():
    """Renumber chapters.
    
    Public methods:
        run(sourcePath, **kwargs) -- Modify chapter headings.
        
    Public instance variables:
        ui -- Ui or YwRenumberTk instance: user interface.
    """

    def __init__(self):
        """Initialize instance variables."""
        self.ui = None

    def run(self, sourcePath, **kwargs):
        """Modify chapter headings.
        
        Positional arguments:
            sourcePath -- str: path to the yWriter project file.
        
        Required keyword arguments:
            ren_regular -- bool: include regular chapters.
            ren_unused -- bool: include chapters marked "Unused" in yWriter.
            ren_parts -- bool: include chapters marked "This chapter begins a new section" in yWriter.
            ren_within_parts -- bool: Reset the chapter number after section beginnings.
            numbering_style -- str: '0'=Arabic numbers; '1'= Roman numbers; '2'= Written out in English.
            numbering_case -- str: '0'=Uppercase; '1'=Capitalized; '2'=Lowercase.
            heading_prefix -- str: a string preceding each number.
            heading_suffix -- str: a string following each number.
        """
        ROMAN = [
            (1000, "m"),
            (900, "cm"),
            (500, "d"),
            (400, "cd"),
            (100, "c"),
            (90, "xc"),
            (50, "l"),
            (40, "xl"),
            (10, "x"),
            (9, "ix"),
            (5, "v"),
            (4, "iv"),
            (1, "i"),
        ]

        def number_to_roman(n):
            """Return n as a Roman number.
            
            Credit goes to the user 'Aristide' on stack overflow.
            https://stackoverflow.com/a/47713392
            """
            result = []
            for (arabic, roman) in ROMAN:
                (factor, n) = divmod(n, arabic)
                result.append(roman * factor)
                if n == 0:
                    break

            return "".join(result)

        TENS = {30: 'thirty', 40: 'forty', 50: 'fifty',
                60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'}
        ZERO_TO_TWENTY = (
            'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
            'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty'
        )

        def number_to_english(n):
            """Return n as a number written out in English.
            
            Credit goes to the user 'Hunter_71' on stack overflow.
            https://stackoverflow.com/a/51849443
            """
            if any(not x.isdigit() for x in str(n)):
                return ''
            if n <= 20:
                return ZERO_TO_TWENTY[n]
            elif n < 100 and n % 10 == 0:
                return TENS[n]
            elif n < 100:
                return f'{number_to_english(n - (n % 10))} {number_to_english(n % 10)}'
            elif n < 1000 and n % 100 == 0:
                return f'{number_to_english(n / 100)} hundred'
            elif n < 1000:
                return f'{number_to_english(n / 100)} hundred {number_to_english(n % 100)}'
            elif n < 1000000:
                return f'{number_to_english(n / 1000)} thousand {number_to_english(n % 1000)}'
            return ''

        self.newFile = None
        __, fileExtension = os.path.splitext(sourcePath)
        if not fileExtension == Yw7File.EXTENSION:
            self.ui.set_info_how(
                f'{ERROR}File "{os.path.normpath(sourcePath)}" is not a yWriter 7 project.')
            return

        if not os.path.isfile(sourcePath):
            self.ui.set_info_how(
                f'{ERROR}File "{os.path.normpath(sourcePath)}" not found.')
            return

        source = Yw7File(sourcePath, **kwargs)
        message = source.read()
        if message.startswith(ERROR):
            self.ui.set_info_how(message)
            return

        i = 0
        for chId in source.srtChapters:
            if source.chapters[chId].chType == 3:
                if not kwargs['ren_unused']:
                    continue

            if source.chapters[chId].isTrash:
                continue

            if source.chapters[chId].chLevel == 0:
                # Regular chapter
                if not kwargs['ren_regular']:
                    continue

            else:
                # Part (chapter "beginning a new section")
                if kwargs['ren_within_parts']:
                    i = 0
                if not kwargs['ren_parts']:
                    continue

            if source.chapters[chId].chType == 0:
                i += 1
                if kwargs['numbering_style'] == '1':
                    number = number_to_roman(i)
                elif kwargs['numbering_style'] == '2':
                    number = number_to_english(i)
                else:
                    number = str(i)
                if kwargs['numbering_case'] == '0':
                    number = number.upper()
                elif kwargs['numbering_case'] == '1':
                    number = number.capitalize()
                source.chapters[chId].title = kwargs['heading_prefix'].replace(
                    '|', '') + number + kwargs['heading_suffix'].replace('|', '')
        message = source.write()
        self.ui.set_info_how(message)
        return
