"""Provide a user interface for chapter renumbering: Tkinter facade

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from pywriter.ui.ui_tk import UiTk


class RnUi(UiTk):
    """Extend the Tkinter GUI, 
    and link it to the application.
    """

    tParts = 'Include Section beginnings'
    tUnused = 'Include "unused" chapters'
    tArabic = 'Arabic numbers'
    tRoman = 'Roman numbers'
    tEnglish = 'Outspelled in English'
    tLowercase = 'Lowercase'
    tUpcase = 'Uppercase'
    tCapitalize = 'Capitalized'
    tPrefix = 'Prefix'
    tSuffix = 'Suffix'
    optionsTotal = 8

    def __init__(self, title, description=None):
        """Make the converter object visible to the user interface 
        in order to make method calls possible.
        Add the widgets needed to invoke the converter manually.
        """
        self.converter = None
        self.infoWhatText = ''
        self.infoHowText = ''
        # UiTk.__init__(self, title)

        self.root = Tk()
        self.root.title(title)

        self.hdTypes = Label(self.root, text='Chapters')
        self.hdOptions = Label(self.root, text='Style')
        self.hdAdd = Label(self.root, text='Add to number')
        self.appInfo = Label(self.root, text='')
        self.appInfo.config(height=2, width=80)

        self.successInfo = Label(self.root)
        self.successInfo.config(height=1, width=80)

        self.processInfo = Label(self.root, text='')

        self.Parts = BooleanVar()
        self.Unused = BooleanVar()
        self.Arabic = BooleanVar()
        self.Roman = BooleanVar()
        self.English = BooleanVar()
        self.Upcase = BooleanVar()
        self.Capitalize = BooleanVar()
        self.Lowercase = BooleanVar()
        self.Prefix = StringVar()
        self.Suffix = StringVar()

        self.root.PartsCheckbox = ttk.Checkbutton(
            text=self.tParts, variable=self.Parts, onvalue=True, offvalue=False)
        self.root.UnusedCheckbox = ttk.Checkbutton(
            text=self.tUnused, variable=self.Unused, onvalue=True, offvalue=False)

        self.root.ArabicCheckbox = ttk.Checkbutton(
            text=self.tArabic, variable=self.Arabic, onvalue=True, offvalue=False)
        self.root.RomanCheckbox = ttk.Checkbutton(
            text=self.tRoman, variable=self.Roman, onvalue=True, offvalue=False)
        self.root.EnglishCheckbox = ttk.Checkbutton(
            text=self.tEnglish, variable=self.English, onvalue=True, offvalue=False)

        self.root.UpcaseCheckbox = ttk.Checkbutton(
            text=self.tUpcase, variable=self.Upcase, onvalue=True, offvalue=False)
        self.root.CapitalizeCheckbox = ttk.Checkbutton(
            text=self.tCapitalize, variable=self.Capitalize, onvalue=True, offvalue=False)
        self.root.LowercaseCheckbox = ttk.Checkbutton(
            text=self.tLowercase, variable=self.Lowercase, onvalue=True, offvalue=False)

        self.root.selectButton = Button(
            text="Select file", command=self.select_file)
        self.root.selectButton.config(height=1, width=20)

        self.root.runButton = Button(
            text='Renumber chapters', command=self.convert_file)
        self.root.runButton.config(height=1, width=20)
        self.root.runButton.config(state='disabled')

        self.root.quitButton = Button(text='Quit', command=self.stop)
        self.root.quitButton.config(height=1, width=20)

        rowCnt = 1
        self.hdTypes.grid(row=rowCnt, column=1, sticky=W,
                          padx=20)
        rowCnt += 1
        self.root.PartsCheckbox.grid(
            row=rowCnt, column=1, sticky=W, padx=20)
        rowCnt += 1
        self.root.UnusedCheckbox.grid(
            row=rowCnt, column=1, sticky=W, padx=20)

        rowCnt = 1
        self.hdOptions.grid(row=rowCnt, column=2, sticky=W,
                            padx=20)
        rowCnt += 1
        self.root.ArabicCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.RomanCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.EnglishCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.UpcaseCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.CapitalizeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.LowercaseCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)

        rowCnt += 1
        self.appInfo.grid(row=rowCnt, column=1,
                          columnspan=3, pady=10)

        rowCnt += 1
        self.root.selectButton.grid(
            row=rowCnt, column=1, padx=10, pady=10, sticky=W)
        self.root.runButton.grid(row=rowCnt, column=2,
                                 padx=10, pady=10, sticky=E)
        self.root.quitButton.grid(
            row=rowCnt, column=3, padx=10, pady=10, sticky=E)

        rowCnt += 1
        self.successInfo.grid(row=rowCnt, column=1, columnspan=3)

        rowCnt += 1
        self.processInfo.grid(row=rowCnt, column=1,
                              columnspan=3, pady=10)

        self.sourcePath = None
        self.set_info_what('No file selected')
        self.startDir = os.getcwd()

        self.filters = {}

    def start(self):
        """Start the user interface.
        Note: This can not be done in the __init__() method.
        """
        self.root.mainloop()

    def stop(self):
        """Stop the user interface.
        """
        self.root.destroy()

    def select_file(self):
        """Open a file dialog in order to set the sourcePath property.
        """
        self.processInfo.config(text='')
        self.successInfo.config(
            bg=self.root.cget("background"))

        if self.sourcePath is not None:
            self.startDir = os.path.dirname(self.sourcePath)

        file = filedialog.askopenfile(initialdir=self.startDir)

        if file:
            self.sourcePath = file.name

        if self.sourcePath:
            self.set_info_what(
                'File: ' + os.path.normpath(self.sourcePath))
            self.root.runButton.config(state='normal')

        else:
            self.set_info_what('No file selected')
            self.root.runButton.config(state='disabled')

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected.
        """

        self.processInfo.config(text='')
        self.successInfo.config(
            bg=self.root.cget("background"))

        if self.sourcePath:
            kwargs = {'parts': self.Parts.get(),
                      'unused': self.Unused.get(),
                      'roman': self.Roman.get(),
                      'english': self.English.get(),
                      'upcase': self.Upcase.get(),
                      'capitalize': self.Capitalize.get(),
                      'prefix': self.Prefix.get(),
                      'suffix': self.Suffix.get(),
                      }
            self.converter.run(self.sourcePath, **kwargs)

            if self.converter.newFile is not None:
                webbrowser.open(self.converter.newFile)
