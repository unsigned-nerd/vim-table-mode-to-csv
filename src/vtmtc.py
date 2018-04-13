#!/usr/bin/env python3

import re
import sys

def vimtable_to_line_list(vimtable):

    # common regexp patterns
    line_sep_pattern = re.compile("^[ ]*\|[\-\+]+\|[ ]*$")
    empty_str_pattern = re.compile("^[ ]*$")

    line = None # each line of vimtable

    # skip until we find a table
    for line in vimtable:
        if line_sep_pattern.match(line):
            break

    # calculate number of columns
    no_of_cols = line.count('+') + 1

    # walk through the table
    for line in vimtable:
        # each line inside vim table starts with |
        line_inside_vimtable_pattern = re.compile("^[ ]*\|.*$")
        if not line_inside_vimtable_pattern.match(line):
            # end of table
            break

        a_row_list = ['' for i in range(no_of_cols)]
        separated_lines = line.split('|')
        for col in range(no_of_cols):
            a_row_list[col] += separated_lines[col+1].lstrip().rstrip()
            print('a_row_list[' + str(col) + ']=' + a_row_list[col])

        # walk through a row
        for line in vimtable:
            if line_sep_pattern.match(line):
                # end of row
                break
            separated_lines = line.split('|')
            for col in range(no_of_cols):
                if not empty_str_pattern.match(separated_lines[col+1]):
                    a_row_list[col] += \
                      ' ' + separated_lines[col+1].lstrip().rstrip()
                print('a_row_list[' + str(col) + ']=' + a_row_list[col])
        yield a_row_list

def _run(argv):
    """
    When calling this script from a command line shell, the top level
    code passes all the work to this function so that we can write a
    test easier for command line application.

    This function returns an output string which is to be printed to
    STDOUT by the top level code.
    """

    if len(argv) == 1:
        return 'Usage: vtmtc.py [FILE]'

    return ''

if __name__ == '__main__':
    stdout_msg = _run(sys.argv)
    if (stdout_msg): print(stdout_msg)
