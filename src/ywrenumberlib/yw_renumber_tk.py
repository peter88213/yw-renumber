#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter chapter renumbering.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.ui.main_tk import MainTk
from ywrenumberlib.config_renumber import ConfigRenumber


class YwRenumberTk(MainTk):
    """A tkinter GUI class for yWriter chapter renumbering."""

    def __init__(self, title, converter, **kwargs):
        """Add widgets for options and settings to the GUI main window.
        
        Positional arguments:
            title -- Application title to be displayed at the window frame.
            converter -- Reference to the YwRn instance.

        optional arguments:
            kwargs -- Keyword argument dictionary containing the configuration.
        Extends the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.converter = converter
        self._configurator = ConfigRenumber()
        self._configurator.show_configuration(self._mainWindow, kwargs)

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
        self.kwargs['yw_last_open'] = self.ywPrj.filePath
        self._configurator.update_configuration(self.kwargs)
        self.converter.run(self.ywPrj.filePath, **self.kwargs)

    def on_quit(self, event=None):
        """Save keyword arguments before exiting the program."""
        self._configurator.update_configuration(self.kwargs)
        super().on_quit(self)
