#!/usr/bin/env python3
""""Provide a tkinter configurator dialog for chapter renumbering.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk


class ConfigRenumber:
    """A tkinter window for configuring chapter renumbering.
    
    Public methods:
        show_configuration(window, kwargs) -- Show a configuration dialog.
        update_configuration(self, kwargs) -- Write options and settings to the applicaton's keyword arguments.
    """

    def show_configuration(self, window, kwargs):
        """Show a configuration dialog.
        
        Positional arguments:
            window -- tk window for the configuration dialog.      
        
        Required keyword arguments:
            ren_unused -- bool: include chapters marked "Unused" in yWriter.
            ren_parts -- bool: include chapters marked "This chapter begins a new section" in yWriter.
            numbering_style -- str: '0'=Arabic numbers; '1'= Roman numbers; '2'= Written out in English.
            numbering_case -- str: '0'=Uppercase; '1'=Capitalized; '2'=Lowercase.
            heading_prefix -- str: a string preceding each number.
            heading_suffix -- str: a string following each number.
        """
        #--- Row 1: Chapters (parts, unused)
        row1Cnt = 1
        hdTypes = tk.Label(window, text='Chapters')
        hdTypes.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._renParts = tk.BooleanVar(value=kwargs['ren_parts'])
        partsCheckbox = ttk.Checkbutton(window, text='Include Section beginnings',
                                        variable=self._renParts, onvalue=True, offvalue=False)
        partsCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)
        row1Cnt += 1
        self._renUnused = tk.BooleanVar(value=kwargs['ren_unused'])
        unusedCheckbox = ttk.Checkbutton(window, text='Include unused chapters',
                                         variable=self._renUnused, onvalue=True, offvalue=False)
        unusedCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        #--- Row 2: Numbering style (numbers, case)
        row2Cnt = 1
        hdOptions = tk.Label(window, text='Numbering style')
        hdOptions.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._numberingStyle = tk.IntVar(value=kwargs['numbering_style'])
        arabicCheckbox = ttk.Radiobutton(window, text='Arabic numbers', variable=self._numberingStyle, value=0)
        arabicCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        romanCheckbox = ttk.Radiobutton(window, text='Roman numbers', variable=self._numberingStyle, value=1)
        romanCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        englishCheckbox = ttk.Radiobutton(window, text='Written out in English',
                                          variable=self._numberingStyle, value=2)
        englishCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        self._numberingCase = tk.IntVar(value=kwargs['numbering_case'])
        upcaseCheckbox = ttk.Radiobutton(window, text='Uppercase', variable=self._numberingCase, value=0)
        upcaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        capitalizeCheckbox = ttk.Radiobutton(window, text='Capitalized', variable=self._numberingCase, value=1)
        capitalizeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)
        row2Cnt += 1
        lowercaseCheckbox = ttk.Radiobutton(window, text='Lowercase', variable=self._numberingCase, value=2)
        lowercaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 3: "Add to number" (Prefix, Suffix)
        row3Cnt = 1
        hdAdd = tk.Label(window, text='Add to number')
        hdAdd.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        hdPrefix = tk.Label(window, text='Prefix')
        hdPrefix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._headingPrefix = tk.StringVar(value=kwargs['heading_prefix'].replace('|', ''))
        prefixEntry = tk.Entry(window, textvariable=self._headingPrefix)
        prefixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        hdSuffix = tk.Label(window, text='Suffix')
        hdSuffix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)
        row3Cnt += 1
        self._headingSuffix = tk.StringVar(value=kwargs['heading_suffix'].replace('|', ''))
        suffixEntry = tk.Entry(window, textvariable=self._headingSuffix)
        suffixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

    def update_configuration(self, kwargs):
        """Write options and settings to the applicaton's keyword arguments.
        
        Positional arguments:
            kwargs -- reference to the ui kwargs dictionary.
        """
        kwargs['ren_parts'] = self._renParts.get()
        kwargs['ren_unused'] = self._renUnused.get()
        kwargs['numbering_style'] = str(self._numberingStyle.get())
        kwargs['numbering_case'] = str(self._numberingCase.get())
        kwargs['heading_prefix'] = f'|{self._headingPrefix.get()}|'
        kwargs['heading_suffix'] = f'|{self._headingSuffix.get()}|'
