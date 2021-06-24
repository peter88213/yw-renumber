"""Provide a user interface for the reporter: Tkinter facade

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from pywriter.ui.ui_tk import UiTk
from pywriter.file.filter import Filter


class RnUi(UiTk):
    """Extend the Tkinter GUI, 
    and link it to the application.
    """

    tShowChapters = 'Include chapters'
    tShowScenes = 'Include scenes'
    levelsTotal = 2
    tShowNormalType = 'Include "normal" type'
    tShowUnusedType = 'Include "unused" type'
    tShowNotesType = 'Include "notes" type'
    tShowTodoType = 'Include "to do" type'
    tShowUnexported = 'Include "do not export" type'
    typesTotal = 5
    tShowTitle = 'Title'
    tShowDescription = 'Description'
    tShowTags = 'Tags'
    tShowNotes = 'Notes'
    tShowDate = 'Date'
    tShowTime = 'Time'
    tShowDuration = 'Duration'
    tShowActionPattern = 'A/R-Goal-Conflict-Outcome'
    tShowRatings = 'Scene ratings'
    tShowWordcount = 'Word count'
    tShowLettercount = 'Letter count'
    tShowStatus = 'Status'
    tShowViewpoint = 'Viewpoint'
    tShowCharacters = 'Characters'
    tShowLocations = 'Locations'
    tShowItems = 'Items'
    columnsTotal = 16

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

        self.hdLevels = Label(self.root, text='Levels')
        self.hdTypes = Label(self.root, text='Types')
        self.hdColumns = Label(self.root, text='Columns')
        self.appInfo = Label(self.root, text='')
        self.appInfo.config(height=2, width=80)

        self.successInfo = Label(self.root)
        self.successInfo.config(height=1, width=80)

        self.processInfo = Label(self.root, text='')

        self.ShowChapters = BooleanVar()
        self.ShowScenes = BooleanVar()
        self.ShowNormalType = BooleanVar()
        self.ShowUnusedType = BooleanVar()
        self.ShowNotesType = BooleanVar()
        self.ShowTodoType = BooleanVar()
        self.ShowUnexported = BooleanVar()
        self.ShowTitle = BooleanVar()
        self.ShowDescription = BooleanVar()
        self.ShowViewpoint = BooleanVar()
        self.ShowTags = BooleanVar()
        self.ShowNotes = BooleanVar()
        self.ShowDate = BooleanVar()
        self.ShowTime = BooleanVar()
        self.ShowDuration = BooleanVar()
        self.ShowActionPattern = BooleanVar()
        self.ShowRatings = BooleanVar()
        self.ShowWordcount = BooleanVar()
        self.ShowLettercount = BooleanVar()
        self.ShowStatus = BooleanVar()
        self.ShowCharacters = BooleanVar()
        self.ShowLocations = BooleanVar()
        self.ShowItems = BooleanVar()

        self.root.ShowChaptersCheckbox = ttk.Checkbutton(
            text=self.tShowChapters, variable=self.ShowChapters, onvalue=True, offvalue=False)
        self.root.ShowScenesCheckbox = ttk.Checkbutton(
            text=self.tShowScenes, variable=self.ShowScenes, onvalue=True, offvalue=False)
        self.root.ShowNormalTypeCheckbox = ttk.Checkbutton(
            text=self.tShowNormalType, variable=self.ShowNormalType, onvalue=True, offvalue=False)
        self.root.ShowUnusedTypeCheckbox = ttk.Checkbutton(
            text=self.tShowUnusedType, variable=self.ShowUnusedType, onvalue=True, offvalue=False)
        self.root.ShowNotesTypeCheckbox = ttk.Checkbutton(
            text=self.tShowNotesType, variable=self.ShowNotesType, onvalue=True, offvalue=False)
        self.root.ShowTodoTypeCheckbox = ttk.Checkbutton(
            text=self.tShowTodoType, variable=self.ShowTodoType, onvalue=True, offvalue=False)
        self.root.ShowUnexportedCheckbox = ttk.Checkbutton(
            text=self.tShowUnexported, variable=self.ShowUnexported, onvalue=True, offvalue=False)
        self.root.ShowTitleCheckbox = ttk.Checkbutton(
            text=self.tShowTitle, variable=self.ShowTitle, onvalue=True, offvalue=False)
        self.root.ShowDescriptionCheckbox = ttk.Checkbutton(
            text=self.tShowDescription, variable=self.ShowDescription, onvalue=True, offvalue=False)
        self.root.ShowViewpointCheckbox = ttk.Checkbutton(
            text=self.tShowViewpoint, variable=self.ShowViewpoint, onvalue=True, offvalue=False)
        self.root.ShowTagsCheckbox = ttk.Checkbutton(
            text=self.tShowTags, variable=self.ShowTags, onvalue=True, offvalue=False)
        self.root.ShowNotesCheckbox = ttk.Checkbutton(
            text=self.tShowNotes, variable=self.ShowNotes, onvalue=True, offvalue=False)
        self.root.ShowDateCheckbox = ttk.Checkbutton(
            text=self.tShowDate, variable=self.ShowDate, onvalue=True, offvalue=False)
        self.root.ShowTimeCheckbox = ttk.Checkbutton(
            text=self.tShowTime, variable=self.ShowTime, onvalue=True, offvalue=False)
        self.root.ShowDurationCheckbox = ttk.Checkbutton(
            text=self.tShowDuration, variable=self.ShowDuration, onvalue=True, offvalue=False)
        self.root.ShowActionPatternCheckbox = ttk.Checkbutton(
            text=self.tShowActionPattern, variable=self.ShowActionPattern, onvalue=True, offvalue=False)
        self.root.ShowRatingsCheckbox = ttk.Checkbutton(
            text=self.tShowRatings, variable=self.ShowRatings, onvalue=True, offvalue=False)
        self.root.ShowWordcountCheckbox = ttk.Checkbutton(
            text=self.tShowWordcount, variable=self.ShowWordcount, onvalue=True, offvalue=False)
        self.root.ShowLettercountCheckbox = ttk.Checkbutton(
            text=self.tShowLettercount, variable=self.ShowLettercount, onvalue=True, offvalue=False)
        self.root.ShowStatusCheckbox = ttk.Checkbutton(
            text=self.tShowStatus, variable=self.ShowStatus, onvalue=True, offvalue=False)
        self.root.ShowCharactersCheckbox = ttk.Checkbutton(
            text=self.tShowCharacters, variable=self.ShowCharacters, onvalue=True, offvalue=False)
        self.root.ShowLocationsCheckbox = ttk.Checkbutton(
            text=self.tShowLocations, variable=self.ShowLocations, onvalue=True, offvalue=False)
        self.root.ShowItemsCheckbox = ttk.Checkbutton(
            text=self.tShowItems, variable=self.ShowItems, onvalue=True, offvalue=False)

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
        self.hdLevels.grid(row=rowCnt, column=1, sticky=W,
                           padx=20)
        rowCnt += 1
        self.root.ShowChaptersCheckbox.grid(
            row=rowCnt, column=1, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowScenesCheckbox.grid(
            row=rowCnt, column=1, sticky=W, padx=20)

        rowCnt = 1
        self.hdTypes.grid(row=rowCnt, column=2, sticky=W,
                          padx=20)
        rowCnt += 1
        self.root.ShowNormalTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowUnusedTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowNotesTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowTodoTypeCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowUnexportedCheckbox.grid(
            row=rowCnt, column=2, sticky=W, padx=20)

        rowCnt = 1
        self.hdColumns.grid(row=rowCnt, column=3, sticky=W,
                            padx=20)
        rowCnt += 1
        self.root.ShowTitleCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowDescriptionCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowViewpointCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowTagsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowNotesCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowDateCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowTimeCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowDurationCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowActionPatternCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowRatingsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowWordcountCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowLettercountCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowStatusCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowCharactersCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowLocationsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)
        rowCnt += 1
        self.root.ShowItemsCheckbox.grid(
            row=rowCnt, column=3, sticky=W, padx=20)

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
        sceneFilter = Filter()

        self.processInfo.config(text='')
        self.successInfo.config(
            bg=self.root.cget("background"))

        if self.sourcePath:
            kwargs = {'sceneFilter': sceneFilter,
                      'showChapters': self.ShowChapters.get(),
                      'showScenes': self.ShowScenes.get(),
                      'showNormalType': self.ShowNormalType.get(),
                      'showUnusedType': self.ShowUnusedType.get(),
                      'showNotesType': self.ShowNotesType.get(),
                      'showTodoType': self.ShowTodoType.get(),
                      'showUnexported': self.ShowUnexported.get(),
                      'showTitle': self.ShowTitle.get(),
                      'showDescription': self.ShowDescription.get(),
                      'showViewpoint': self.ShowViewpoint.get(),
                      'showTags': self.ShowTags.get(),
                      'showNotes': self.ShowNotes.get(),
                      'showDate': self.ShowDate.get(),
                      'showTime': self.ShowTime.get(),
                      'showDuration': self.ShowDuration.get(),
                      'showActionPattern': self.ShowActionPattern.get(),
                      'showRatings': self.ShowRatings.get(),
                      'showWordcount': self.ShowWordcount.get(),
                      'showLettercount': self.ShowLettercount.get(),
                      'showStatus': self.ShowStatus.get(),
                      'showCharacters': self.ShowCharacters.get(),
                      'showLocations': self.ShowLocations.get(),
                      'showItems': self.ShowItems.get(),
                      }
            self.converter.run(self.sourcePath, **kwargs)

            if self.converter.newFile is not None:
                webbrowser.open(self.converter.newFile)
