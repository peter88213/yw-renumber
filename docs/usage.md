[Project homepage](https://peter88213.github.io/yw-renumber)

--- 

The *yw-renumber* Python script rewrites chapter titles in yWriter 7 projects.

## Usage

The included installation script prompts you to create a shortcut on the desktop. 

You can either

- launch the program by double-clicking on the program/link icon, or
- launch the program by dragging a yWriter project file and dropping it on the program/link icon.

*yw-renumber* processes .yw7 project files. If no yWriter project is specified by dragging and dropping on the program icon, the latest project selected is preset. You can change it with **Select File**.

The style options are set by ticking checkboxes and filling out forms. On program startup, the latest options selected are preset.



### Operation

#### Open a yWriter project

- If no yWriter project is specified by dragging and dropping on the program icon, the latest project selected is preset. You can change it with **File > Open** or **Ctrl-O***.

#### Start renumbering

- When the yWriter project is selected and the options are set, you can launch the renumbering with **Renumber chapters** *(Alt-R)*. The new chapter titles are written directly into the yWriter project file.
- If the project is open in yWriter, you will be asked to exit yWriter first.

#### Close the ywriter project

- You can close the project without exiting the program with **File > Close**.
- If you open another project, the current project is automatically closed.

#### Exit 

- You can exit with **File > Exit** or **Ctrl-Q**.

### Options

#### Chapters

By default, all normal chapters are renumbered, which are displayed in thin green text in the yWriter chapter list. If you wish to exclude chapters from the numbering, you can change temporarily their type to *"ToDo"* or *"Notes"*, or mark them temporarily *"unused"*. Another option is to mark them as *section beginnings* (see below).

- **Include regular chapters** -- Include chapters that don't begin a new section.
- **Include section beginnings** -- Include parts (chapters marked *"This chapter begins a new section"* in the yWriter chapter dialog).
- **Include "unused" chapters** -- Include chapters marked *"Unused"* in yWriter.
- **Reset number after section beginnings** -- Reset the chapter number when a new part begins.

#### Styles

- **Arabic numbers** -- 1, 2, 3 ...
- **Roman numbers** -- I, II, III ... (case can be set)
- **Written out in English** -- ONE, TWO, THREE ... (case can be set)
- **Uppercase** -- All characters of the number are uppercase.
- **Capitalized** -- The first character of the number is uppercase, the others are lowercase.
- **Lowercase** -- All characters of the number are lowercase.

Note: The case options do not apply to the prefix and suffix.

#### Add to number

- **Prefix** -- A string preceding each number.
- **Suffix** -- A string following each number.


## Configuration file

The latest yWriter project selected and the latest options are saved in a configuration file. 

on Windows, this is the file path: 

`c:\Users\<user name>\.pywriter\yw-renumber\config\yw-renumber.ini`

You can safely delete this file at any time.

## Installation path

The setup script installs *yw-renumber.pyw* in the user profile. This is the installation path on windows: 

`c:\Users\<user name>\.pywriter\yw-renumber`

