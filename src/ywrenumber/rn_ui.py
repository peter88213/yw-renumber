"""Provide a Tkinter facade user interface class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from pywriter.ui.ui_tk import UiTk


class RnUi(UiTk):
    """Tkinter based GUI.
    Extend the superclass.
    """

    def __init__(self, title, sourcePath=None, **kwargs):
        """Make the converter object visible to the user interface 
        in order to make method calls possible.
        Add the widgets needed to invoke the converter manually.
        """
        self.kwargs = kwargs
        self.converter = None
        self.infoWhatText = ''
        self.infoHowText = ''

        self.root = tk.Tk()
        self.root.title(title)

        #--- Row 1: Chapters (parts, unused)

        row1Cnt = 1
        self.hdTypes = tk.Label(self.root, text='Chapters')
        self.hdTypes.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self.renParts = tk.BooleanVar(value=kwargs['ren_parts'])
        self.partsCheckbox = ttk.Checkbutton(
            text='Include Section beginnings', variable=self.renParts, onvalue=True, offvalue=False)
        self.partsCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        row1Cnt += 1
        self.renUnused = tk.BooleanVar(value=kwargs['ren_unused'])
        self.unusedCheckbox = ttk.Checkbutton(
            self.root, text='Include "unused" chapters', variable=self.renUnused, onvalue=True, offvalue=False)
        self.unusedCheckbox.grid(row=row1Cnt, column=1, sticky=tk.W, padx=20)

        #--- Row 2: Numbering style (numbers, case)

        row2Cnt = 1
        self.hdOptions = tk.Label(self.root, text='Numbering style')
        self.hdOptions.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.numberingStyle = tk.IntVar(value=kwargs['numberingStyle'])
        self.arabicCheckbox = ttk.Radiobutton(self.root, text='Arabic numbers', variable=self.numberingStyle, value=0)
        self.arabicCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.romanCheckbox = ttk.Radiobutton(self.root, text='Roman numbers', variable=self.numberingStyle, value=1)
        self.romanCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.englishCheckbox = ttk.Radiobutton(
            self.root, text='Written out in English', variable=self.numberingStyle, value=2)
        self.englishCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.numberingCase = tk.IntVar(value=kwargs['numberingCase'])
        self.upcaseCheckbox = ttk.Radiobutton(self.root, text='Uppercase', variable=self.numberingCase, value=0)
        self.upcaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.capitalizeCheckbox = ttk.Radiobutton(self.root, text='Capitalized', variable=self.numberingCase, value=1)
        self.capitalizeCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        row2Cnt += 1
        self.lowercaseCheckbox = ttk.Radiobutton(self.root, text='Lowercase', variable=self.numberingCase, value=2)
        self.lowercaseCheckbox.grid(row=row2Cnt, column=2, sticky=tk.W, padx=20)

        #--- Row 3: "Add to number" (Prefix, Suffix)

        row3Cnt = 1
        self.hdAdd = tk.Label(self.root, text='Add to number')
        self.hdAdd.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.hdPrefix = tk.Label(self.root, text='Prefix')
        self.hdPrefix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.headingPrefix = tk.StringVar(value=kwargs['headingPrefix'].replace('|', ''))
        self.prefixEntry = tk.Entry(self.root, textvariable=self.headingPrefix)
        self.prefixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.hdSuffix = tk.Label(self.root, text='Suffix')
        self.hdSuffix.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        row3Cnt += 1
        self.headingSuffix = tk.StringVar(value=kwargs['headingSuffix'].replace('|', ''))
        self.suffixEntry = tk.Entry(self.root, textvariable=self.headingSuffix)
        self.suffixEntry.grid(row=row3Cnt, column=3, sticky=tk.W, padx=20)

        if row3Cnt > row2Cnt:
            rowCnt = row3Cnt

        else:
            rowCnt = row2Cnt

        if row1Cnt > rowCnt:
            rowCnt = row1Cnt

        rowCnt += 1
        self.appInfo = tk.Label(self.root, text='')
        self.appInfo.config(height=2, width=75)
        self.appInfo.grid(row=rowCnt, column=1, columnspan=3, pady=10)

        rowCnt += 1
        self.selectButton = tk.Button(self.root, text="Select file", command=self.select_file)
        self.selectButton.config(height=1, width=20)
        self.selectButton.grid(row=rowCnt, column=1, padx=10, pady=10, sticky=tk.W)

        self.runButton = tk.Button(self.root, text='Renumber chapters', command=self.convert_file)
        self.runButton.config(height=1, width=20)
        self.runButton.config(state='disabled')
        self.runButton.grid(row=rowCnt, column=2, padx=10, pady=10, sticky=tk.E)

        self.quitButton = tk.Button(self.root, text='Quit', command=self.stop)
        self.quitButton.config(height=1, width=20)
        self.quitButton.grid(row=rowCnt, column=3, padx=10, pady=10, sticky=tk.E)

        rowCnt += 1
        self.successInfo = tk.Label(self.root)
        self.successInfo.config(height=1, width=75)
        self.successInfo.grid(row=rowCnt, column=1, columnspan=3)

        rowCnt += 1
        self.processInfo = tk.Label(self.root, text='')
        self.processInfo.grid(row=rowCnt, column=1, columnspan=3, pady=10)

        self.sourcePath = None

        if kwargs['yw_last_open']:

            if os.path.isfile(kwargs['yw_last_open']):
                self.sourcePath = kwargs['yw_last_open']

        if sourcePath:

            if os.path.isfile(sourcePath):
                self.sourcePath = sourcePath

        if self.sourcePath is not None:
            self.set_info_what('File: ' + os.path.normpath(self.sourcePath))
            self.runButton.config(state='normal')

        else:
            self._sourcePath = None
            self.set_info_what('No file selected')
            self.startDir = os.getcwd()

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
        self.successInfo.config(bg=self.root.cget("background"))

        if self.sourcePath is not None:
            self.startDir = os.path.dirname(self.sourcePath)

        file = filedialog.askopenfile(initialdir=self.startDir)

        if file:
            self.sourcePath = file.name

        if self.sourcePath:
            self.set_info_what('File: ' + os.path.normpath(self.sourcePath))
            self.root.runButton.config(state='normal')

        else:
            self.set_info_what('No file selected')
            self.root.runButton.config(state='disabled')

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected.
        """
        self.processInfo.config(text='')
        self.successInfo.config(bg=self.root.cget("background"))

        if self.sourcePath:
            self.kwargs = dict(
                yw_last_open=self.sourcePath,
                ren_parts=self.renParts.get(),
                ren_unused=self.renUnused.get(),
                numberingStyle=str(self.numberingStyle.get()),
                numberingCase=str(self.numberingCase.get()),
                headingPrefix='|' + self.headingPrefix.get() + '|',
                headingSuffix='|' + self.headingSuffix.get() + '|',
            )
            self.converter.run(self.sourcePath, **self.kwargs)

            if self.converter.newFile is not None:
                webbrowser.open(self.converter.newFile)
