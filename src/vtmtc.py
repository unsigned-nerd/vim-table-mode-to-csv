#!/usr/bin/env python3

import re
import sys

def vimtable_to_col_list(vimtable):

    # common regexp patterns which are used in this function
    line_sep_pattern = re.compile("^[ ]*\|[\-\+]+\|[ ]*$")
    empty_str_pattern = re.compile("^[ ]*$")

    line = None # each line of vimtable we are walking through

    # walk through each line until we reach a table
    for line in vimtable:
        if line_sep_pattern.match(line):
            # found the line that looks something like this, |----+----|
            break

    # calculate number of columns by counting the number of plus sign
    # (+) on the 'line seperation' line we have found above
    no_of_cols = line.count('+') + 1

    # walk through the table, one iteration per row
    for line in vimtable:
        # each line inside vim table starts with |
        line_inside_vimtable_pattern = re.compile("^[ ]*\|.*$")
        if not line_inside_vimtable_pattern.match(line):
            # end of table
            break

        # let's build a row (list to yield)
        row = ['' for i in range(no_of_cols)]

        # for the first line of the row
        splitted_line = line.split('|')
        for col in range(no_of_cols):
            row[col] += splitted_line[col+1].lstrip().rstrip()

        # walk through the rest lines of this row
        for line in vimtable:
            if line_sep_pattern.match(line):
                # end of row
                break
            splitted_line = line.split('|')
            for col in range(no_of_cols):
                if empty_str_pattern.match(splitted_line[col+1]):
                    continue # do nothing if it is an empty line

                if not empty_str_pattern.match(row[col]):
                    row[col] += ' '

                row[col] += splitted_line[col+1].lstrip().rstrip()

        yield row

def vimtable_col_list_to_csv_line(row):
    line = ''
    for col in row:
        col = col.replace('"', '""')
        if ',' in col:
            line += '"' + col + '",'
        else:
            line += col + ","
    return line

def vimtablefiletocsvfile(vimtable_file, csv_file):
    vimtable = open(vimtable_file)
    with open(csv_file, 'w') as _csv_file:
        for row in vimtable_to_col_list(vimtable):
            _csv_file.write(vimtable_col_list_to_csv_line(row) + '\n')
    vimtable.close()

def _run(argv):
    """
    When calling this script from a command line shell, the top level
    code passes all the work to this function so that we can write a
    test easier for command line application.

    This function returns an output string which is to be printed to
    STDOUT by the top level code.
    """

    if len(argv) < 3:
        return 'Usage: vtmtc.py [IN_FILE] [OUT_FILE]'

    vimtablefiletocsvfile(argv[1], argv[2])

if __name__ == '__main__':
    stdout_msg = _run(sys.argv)
    if (stdout_msg): print(stdout_msg)
