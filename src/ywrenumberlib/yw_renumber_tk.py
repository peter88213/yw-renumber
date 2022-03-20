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
    """A tkinter GUI class for yWriter chapter renumbering."""

    def __init__(self, title, **kwargs):
        """Add widgets for options and settings to the GUI main window.
        
        Positional argument:
            title -- application title to be displayed at the window frame.

        Required keyword arguments:
            ren_unused -- bool: include chapters marked "Unused" in yWriter.
            ren_parts -- bool: include chapters marked "This chapter begins a new section" in yWriter.
            numbering_style -- str: '0'=Arabic numbers; '1'= Roman numbers; '2'= Written out in English.
            numbering_case -- str: '0'=Uppercase; '1'=Capitalized; '2'=Lowercase.
            heading_prefix -- str: a string preceding each number.
            heading_suffix -- str: a string following each number.
        
        Get the keyword arguments for widget initialization.
        Extends the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.converter = None

        #--- Row 1: Chapters (parts, unused)
        row1Cnt = 1
        hdTypes = tk.Label(self._mainWindow, text='Chapters')
        hdTypes.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._renParts = tk.BooleanVar(value=kwargs['ren_parts'])
        partsCheckbox = ttk.Checkbutton(self._mainWindow, text='Include Section beginnings',
                                        variable=self._renParts, onvalue=True, offvalue=False)
        partsCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._renUnused = tk.BooleanVar(value=kwargs['ren_unused'])
        unusedCheckbox = ttk.Checkbutton(self._mainWindow, text='Include unused chapters',
                                         variable=self._renUnused, onvalue=True, offvalue=False)
        unusedCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        #--- Row 2: Numbering style (numbers, case)
        row2Cnt = 1
        hdOptions = tk.Label(self._mainWindow, text='Numbering style')
        hdOptions.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._numberingStyle = tk.IntVar(value=kwargs['numbering_style'])
        arabicCheckbox = ttk.Radiobutton(self._mainWindow, text='Arabic numbers', variable=self._numberingStyle, value=0)
        arabicCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        romanCheckbox = ttk.Radiobutton(self._mainWindow, text='Roman numbers', variable=self._numberingStyle, value=1)
        romanCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        englishCheckbox = ttk.Radiobutton(self._mainWindow, text='Written out in English',
                                          variable=self._numberingStyle, value=2)
        englishCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._numberingCase = tk.IntVar(value=kwargs['numbering_case'])
        upcaseCheckbox = ttk.Radiobutton(self._mainWindow, text='Uppercase', variable=self._numberingCase, value=0)
        upcaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        capitalizeCheckbox = ttk.Radiobutton(self._mainWindow, text='Capitalized', variable=self._numberingCase, value=1)
        capitalizeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        lowercaseCheckbox = ttk.Radiobutton(self._mainWindow, text='Lowercase', variable=self._numberingCase, value=2)
        lowercaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 3: "Add to number" (Prefix, Suffix)
        row3Cnt = 1
        hdAdd = tk.Label(self._mainWindow, text='Add to number')
        hdAdd.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        hdPrefix = tk.Label(self._mainWindow, text='Prefix')
        hdPrefix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._headingPrefix = tk.StringVar(value=kwargs['heading_prefix'].replace('|', ''))
        prefixEntry = tk.Entry(self._mainWindow, textvariable=self._headingPrefix)
        prefixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        hdSuffix = tk.Label(self._mainWindow, text='Suffix')
        hdSuffix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._headingSuffix = tk.StringVar(value=kwargs['heading_suffix'].replace('|', ''))
        suffixEntry = tk.Entry(self._mainWindow, textvariable=self._headingSuffix)
        suffixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

    def _build_main_menu(self):
        """Add main menu entries.
        
        Extends the superclass template method. 
        """
        super()._build_main_menu()
        self._mainMenu.add_command(label='Renumber chapters', command=self._convert_file)
        self._mainMenu.entryconfig('Renumber chapters', state='disabled')

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('Renumber chapters', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('Renumber chapters', state='normal')

    def _convert_file(self):
        """Call the converter's conversion method.
        
        Write selected options and settings to the keyword arguments.
        Overrides the superclass method.
        """
        self.kwargs['yw_last_open'] = self._ywPrj.filePath
        self.kwargs['ren_parts'] = self._renParts.get()
        self.kwargs['ren_unused'] = self._renUnused.get()
        self.kwargs['numbering_style'] = str(self._numberingStyle.get())
        self.kwargs['numbering_case'] = str(self._numberingCase.get())
        self.kwargs['heading_prefix'] = f'|{self._headingPrefix.get()}|'
        self.kwargs['heading_suffix'] = f'|{self._headingSuffix.get()}|'
        self.converter.run(self._ywPrj.filePath, **self.kwargs)
