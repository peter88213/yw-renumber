"""HTML report from yWriter. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw-reporter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.file.file_export import FileExport


class HtmlReport(FileExport):
    """Export content or metadata from an yWriter project to a HTML file.
    """

    DESCRIPTION = 'HTML report'
    EXTENSION = '.html'
    SUFFIX = '_report'

    fileHeader = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

<style type="text/css">
body {font-family: sans-serif}
p.title {font-size: larger; font-weight: bold}
p.author {font-style: italic}
td, th {padding: 10}
th {font-size:smaller}
table {border-spacing: 0}
table, th, td {border: lightgrey solid 1px; vertical-align: top}
td.chtitle {font-weight: bold}
td.chdesc {font-style: italic}
tr.part {font-weight: bold}
tr.unused {color:gray}
tr.notes {color:blue}
tr.todo {color:firebrick}
tr.notexp {font-style: italic}
</style>

<title>$Title</title>
</head>

<body>
<p class=title>$Title</p>
<p class=author>$AuthorName</p>
<br />
<table>
'''

    fileFooter = '''</table>
</body>
</html>
'''

    def __init__(self, filePath, **kwargs):
        FileExport.__init__(self, filePath)

        self.sceneFilter = kwargs['sceneFilter']

        hdColumns = []
        chColumns = []
        scColumns = []

        if kwargs['showTitle']:
            hdColumns.append('<th>Title</th>')
            chColumns.append('<td class="chtitle">$Title</td>')
            scColumns.append('<td>$Title</td>')

        if kwargs['showDescription']:
            hdColumns.append('<th>Description</th>')
            chColumns.append('<td class="chdesc">$Desc</td>')
            scColumns.append('<td>$Desc</td>')

        if kwargs['showViewpoint']:
            hdColumns.append('<th>Viewpoint</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Viewpoint</td>')

        if kwargs['showTags']:
            hdColumns.append('<th>Tags</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Tags</td>')

        if kwargs['showNotes']:
            hdColumns.append('<th>Notes</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Notes</td>')

        if kwargs['showDate']:
            hdColumns.append('<th>Date</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$ScDate</td>')

        if kwargs['showTime']:
            hdColumns.append('<th>Time</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$ScTime</td>')

        if kwargs['showDuration']:
            hdColumns.append('<th>Duration</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Duration</td>')

        if kwargs['showActionPattern']:
            hdColumns.append('<th>A/R</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$ReactionScene</td>')
            hdColumns.append('<th>Goal</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Goal</td>')
            hdColumns.append('<th>Conflict</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Conflict</td>')
            hdColumns.append('<th>Outcome</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Outcome</td>')

        if kwargs['showRatings']:
            hdColumns.append('<th>$FieldTitle1</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field1</td>')
            hdColumns.append('<th>$FieldTitle2</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field2</td>')
            hdColumns.append('<th>$FieldTitle3</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field3</td>')
            hdColumns.append('<th>$FieldTitle4</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Field4</td>')

        if kwargs['showWordcount']:
            hdColumns.append('<th>Word count</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$WordCount</td>')

        if kwargs['showLettercount']:
            hdColumns.append('<th>Letter count</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$LetterCount</td>')

        if kwargs['showStatus']:
            hdColumns.append('<th>Status</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Status</td>')

        if kwargs['showCharacters']:
            hdColumns.append('<th>Characters</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Characters</td>')

        if kwargs['showLocations']:
            hdColumns.append('<th>Locations</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Locations</td>')

        if kwargs['showItems']:
            hdColumns.append('<th>Items</th>')
            chColumns.append('<td></td>')
            scColumns.append('<td>$Items</td>')

        hdRow = ''.join(hdColumns)
        chRow = ''.join(chColumns)
        scRow = ''.join(scColumns)

        self.fileHeader += '<thead><tr>' + hdRow + '</tr></thead>'

        if kwargs['showChapters']:

            if kwargs['showNormalType']:
                self.chapterTemplate = '<tr>' + chRow + '</tr>'
                self.partTemplate = '<tr class="part">' + chRow + '</tr>'

            if kwargs['showUnusedType']:
                self.unusedChapterTemplate = '<tr class="unused">' + chRow + '</tr>'

            if kwargs['showNotesType']:
                self.notesChapterTemplate = '<tr class="notes">' + chRow + '</tr>'

            if kwargs['showTodoType']:
                self.todoChapterTemplate = '<tr class="todo">' + chRow + '</tr>'

        if kwargs['showScenes']:

            if kwargs['showNormalType']:
                self.sceneTemplate = '<tr>' + scRow + '</tr>'

            if kwargs['showUnusedType']:
                self.unusedSceneTemplate = '<tr class="unused">' + scRow + '</tr>'

            if kwargs['showNotesType']:
                self.notesSceneTemplate = '<tr class="notes">' + scRow + '</tr>'

            if kwargs['showTodoType']:
                self.todoSceneTemplate = '<tr class="todo">' + scRow + '</tr>'

            if kwargs['showUnexported']:
                self.notExportedSceneTemplate = '<tr class="notexp">' + scRow + '</tr>'
