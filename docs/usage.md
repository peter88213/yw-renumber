[Project homepage](https://peter88213.github.io/yw-reporter)

--- 

The *yw-reporter* Python script creates configurable reports from yWriter projects.

## Usage

It is recommended to create a link on the desktop.

You can either

- launch the program by double-clicking on the program/link icon, or
- launch the program by dragging a yWriter project file and dropping it on the program/link icon.

The report generator processes .yw5, .yw6 and .yw7 project files. If no yWriter project is specified by dragging and dropping on the program icon, the latest project selected is preset. You can change it with **Select File**.

The report options are set by ticking checkboxes. On program startup, the latest options selected are preset.

When the yWriter project is selected and the options are set, you can launch the report generator with **Create report**. A HTML report file is created in the yWriter project folder, and a web browser window opens to show it. If a report file already exists, you will be asked before it is overwritten.

If you wish to keep a report, you can save it under a different name from within the web browser.

You can generate as many reports with different options as you like without exiting the program in between. Note, however, that a new tab may be created in the web browser each time, so that you can also see earlier reports for which there is no longer a file.


### Options

#### Level options

- **Include chapters** -- Create table rows for chapters as specified below.
- **Include scenes** -- Create table rows for scenes as specified below.

#### Type options

- **Include normal** -- Create a table row for every "normal" chapter or scene.
- **Include unused** -- Create a table row for every "unused" chapter or scene.
- **Include notes** -- Create a table row for every chapter or scene marked "Notes" or "Info".
- **Include todo** -- Create a table row for every chapter or scene marked "ToDo" (.yw7 only).
- **Include unexported** -- Create table rows for scenes that won't be exported as RTF from yWriter.

#### Columns

- **Title** -- Create a column for chapter/scene titles.
- **Description** -- Create a column for chapter/scene descriptions.
- **Viewpoint** -- Create a column for scene viewpoints.
- **Tags** -- Create a column for scene tags (comma separated).
- **Notes** -- Create a column for scene notes.
- **Date** -- Create a column for either specific date or day.
- **Time** -- Create a column for either specific time or hour/minute.
- **Duration** -- Create a column for days, hours, minutes the scene lasts.
- **A/R-Goal-Conflict-Outcome** -- Create four columns (A/R, Goal etc.) 
- **Ratings** -- Create four columns (scene rating 1-4).
- **Word count** -- Create a column for scene word count.
- **Letter count** -- Create a column for scene letter count.
- **Status** -- Create a column for scene status (Outline, Draft etc.)
- **Characters** -- Create a column for characters in scene (comma separated).
- **Locations** -- Create a column for locations in scene (comma separated).
- **Items** -- Create a column for items in scene (comma separated).


## Configuration file

The latest yWriter project selected and the latest options are saved in a configuration file. 

In Windows, this is the file path: 

`c:\Users\<user name>\AppData\Roaming\yw-reporter\yw-reporter.ini`

You can safely delete this file at any time.
