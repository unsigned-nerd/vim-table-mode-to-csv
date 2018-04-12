#!/usr/bin/env python3

import sys

def collapsemultilines(iterable_multilines_text):
    res_str = """some text

|---------------------------------------------------------------+---------------------------------------------------------------------------|
| Lorem ipsum dolor sit amet                                    | Suspendisse quis ipsum  diam. Etiam tristique libero et imperdiet tempor. |
|---------------------------------------------------------------+---------------------------------------------------------------------------|
| Donec semper augue et metus consequat lobortis quis ac metus. | Quisque sodales rutrum nulla, a pretium dui cursus nec.                   |
|---------------------------------------------------------------+---------------------------------------------------------------------------|

some other text"""

    for line in res_str.split('\n'):
      yield line + '\n'

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
