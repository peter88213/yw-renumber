#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter chapter renumbering.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk

from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File
from pywriter.ui.main_tk import MainTk


class YwRenumberTk(MainTk):
    """A tkinter GUI class for yWriter chapter renumbering.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.converter = None

        #--- Row 1: Chapters (parts, unused)

        row1Cnt = 1
        hdTypes = tk.Label(self.mainWindow, text='Chapters')
        hdTypes.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self.renParts = tk.BooleanVar(value=kwargs['ren_parts'])
        partsCheckbox = ttk.Checkbutton(self.mainWindow, text='Include Section beginnings',
                                        variable=self.renParts, onvalue=True, offvalue=False)
        partsCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self.renUnused = tk.BooleanVar(value=kwargs['ren_unused'])
        unusedCheckbox = ttk.Checkbutton(self.mainWindow, text='Include unused chapters',
                                         variable=self.renUnused, onvalue=True, offvalue=False)
        unusedCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        #--- Row 2: Numbering style (numbers, case)

        row2Cnt = 1
        hdOptions = tk.Label(self.mainWindow, text='Numbering style')
        hdOptions.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.numberingStyle = tk.IntVar(value=kwargs['numberingStyle'])
        arabicCheckbox = ttk.Radiobutton(self.mainWindow, text='Arabic numbers', variable=self.numberingStyle, value=0)
        arabicCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        romanCheckbox = ttk.Radiobutton(self.mainWindow, text='Roman numbers', variable=self.numberingStyle, value=1)
        romanCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        englishCheckbox = ttk.Radiobutton(self.mainWindow, text='Written out in English',
                                          variable=self.numberingStyle, value=2)
        englishCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.numberingCase = tk.IntVar(value=kwargs['numberingCase'])
        upcaseCheckbox = ttk.Radiobutton(self.mainWindow, text='Uppercase', variable=self.numberingCase, value=0)
        upcaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        capitalizeCheckbox = ttk.Radiobutton(self.mainWindow, text='Capitalized', variable=self.numberingCase, value=1)
        capitalizeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        lowercaseCheckbox = ttk.Radiobutton(self.mainWindow, text='Lowercase', variable=self.numberingCase, value=2)
        lowercaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 3: "Add to number" (Prefix, Suffix)

        row3Cnt = 1
        hdAdd = tk.Label(self.mainWindow, text='Add to number')
        hdAdd.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        hdPrefix = tk.Label(self.mainWindow, text='Prefix')
        hdPrefix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.headingPrefix = tk.StringVar(value=kwargs['headingPrefix'].replace('|', ''))
        prefixEntry = tk.Entry(self.mainWindow, textvariable=self.headingPrefix)
        prefixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        hdSuffix = tk.Label(self.mainWindow, text='Suffix')
        hdSuffix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.headingSuffix = tk.StringVar(value=kwargs['headingSuffix'].replace('|', ''))
        suffixEntry = tk.Entry(self.mainWindow, textvariable=self.headingSuffix)
        suffixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

    def extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self.mainMenu.add_command(label='Renumber chapters', command=self.convert_file)
        self.mainMenu.entryconfig('Renumber chapters', state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('Renumber chapters', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('Renumber chapters', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Return the file name.
        Extend the superclass method.
        """
        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self.ywPrj = Yw7File(fileName)
        message = self.ywPrj.read()

        if message.startswith(ERROR):
            self.close_project()
            self.statusBar.config(text=message)
            return ''

        if self.ywPrj.title:
            titleView = self.ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self.ywPrj.author:
            authorView = self.ywPrj.author

        else:
            authorView = 'Unknown author'

        self.titleBar.config(text=titleView + ' by ' + authorView)
        self.enable_menu()
        return fileName

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected.
        """
        self.kwargs = dict(
            yw_last_open=self.ywPrj.filePath,
            ren_parts=self.renParts.get(),
            ren_unused=self.renUnused.get(),
            numberingStyle=str(self.numberingStyle.get()),
            numberingCase=str(self.numberingCase.get()),
            headingPrefix='|' + self.headingPrefix.get() + '|',
            headingSuffix='|' + self.headingSuffix.get() + '|',
        )
        self.converter.run(self.ywPrj.filePath, **self.kwargs)

    def set_info_what(self, message):
        """What's the converter going to do?
        Just a stub here.
        """

    def set_info_how(self, message):
        """How's the converter doing?"""
        self.statusBar.config(text=message)
