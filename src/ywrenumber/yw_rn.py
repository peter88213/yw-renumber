"""Provide a HTML report generator class for yWriter projects. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.yw.yw7_file import Yw7File


class YwRn():
    """Renumber chapters."""

    def __init__(self):
        """Define instance variables."""
        self.ui = None

    def run(self, sourcePath, **kwargs):

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
                return number_to_english(n - (n % 10)) + ' ' + number_to_english(n % 10)

            elif n < 1000 and n % 100 == 0:
                return number_to_english(n / 100) + ' hundred'

            elif n < 1000:
                return number_to_english(n / 100) + ' hundred ' + number_to_english(n % 100)

            elif n < 1000000:
                return number_to_english(n / 1000) + ' thousand ' + number_to_english(n % 1000)

            return ''

        self.newFile = None

        fileName, fileExtension = os.path.splitext(sourcePath)

        if not fileExtension == Yw7File.EXTENSION:
            self.ui.set_info_how(
                'ERROR: File "' + os.path.normpath(sourcePath) + '" is not a yWriter 7 project.')
            return

        if not os.path.isfile(sourcePath):
            self.ui.set_info_how(
                'ERROR: File "' + os.path.normpath(sourcePath) + '" not found.')
            return

        source = Yw7File(sourcePath, **kwargs)

        message = source.read()

        if message.startswith('ERROR'):
            self.ui.set_info_how(message)
            return

        i = 0

        for chId in source.srtChapters:

            if source.chapters[chId].isUnused:

                if not kwargs['ren_unused']:
                    continue

            if source.chapters[chId].isTrash:
                continue

            if source.chapters[chId].chLevel == 1:

                if not kwargs['ren_parts']:
                    continue

            if source.chapters[chId].chType == 0:
                i += 1

                if kwargs['numberingStyle'] == 1:
                    number = number_to_roman(i)

                elif kwargs['numberingStyle'] == 2:
                    number = number_to_english(i)

                else:
                    number = str(i)

                if kwargs['numberingCase'] == 0:
                    number = number.upper()

                elif kwargs['numberingCase'] == 1:
                    number = number.capitalize()

                source.chapters[chId].title = kwargs['headingPrefix'].replace(
                    '"', '') + number + kwargs['headingSuffix'].replace('"', '')

        message = source.write()
        self.ui.set_info_how(message)
        return
