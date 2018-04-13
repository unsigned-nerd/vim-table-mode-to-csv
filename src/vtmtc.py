#!/usr/bin/env python3

import sys

def vimtabletolist(vimtable_itr):
    expected_result = [
        ['Lorem ipsum dolor sit amet', 'Suspendisse diam. Etiam'],
        ['Donec et metus lobortis', 'Quisque nulla, a']]

    return expected_result

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
