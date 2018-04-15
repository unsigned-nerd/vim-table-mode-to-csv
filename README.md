# vim-table-mode-to-csv.py
a script to convert a vim-table-mode table in a file into csv
(comma-separated values) file

vim-table-mode-to-csv.py is a script which converts plain text generated
from [vim-table-mode](https://github.com/dhruvasagar/vim-table-mode)
into a csv file, ready to be imported into any spreadsheet programs such
as LibreOffice Calc or Google Sheets.

# Why do I write this script?
When I have to keep expenses log of a group of people who travel
together, I use vim-table-mode instead of LibreOffice Calc as it is
easier to use Git to track the changes.  After each trip, I have to
convert the plain text file into a spreadsheet file because my clients
would like to read the report in that format and use spreadsheet
formulas to calculate whatever else they may need.

# Platform
I test the script with:

    - Python 3.5.3
    - Subgraph OS 1.0

# Files structure

- sample/
    - vimtablemode.1.in, vimtablemode.in: sample input files which
      contain vim-table-mode table inside it

- test/tmp
    - a directory that a test script uses to store temporary files

- tests.py
    - the top level (and the only test file) test script, run the test
      with `python3 tests.py`

- vtmtc.py
    - the top level script of the program, run it with `python3
      vtmtc.py`
