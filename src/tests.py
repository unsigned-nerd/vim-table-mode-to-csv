#!/usr/bin/env python3

import unittest
import vtmtc

class MyUnitTest(unittest.TestCase):

    def setUp(self):
        pass
  
    def tearDown(self):
        pass

    def test_helpmsg(self):
        """
        If user calls our script without any argument, shows help
        message.  Like this:

          $ vtmtc.py
          Usage: vtmtc.py [FILE]
        """

        script_name = 'vtmtc.py'

        # calling the script without an argument, shows help message

        argv = (script_name, )

        stdout_msg = vtmtc._run(argv)

        expected_stdout_msg = """Usage: vtmtc.py [FILE]"""
        self.assertEqual(expected_stdout_msg, stdout_msg)

        # calling the script with an argument, doesn't show help message

        argv = (script_name, 'hello')

        stdout_msg = vtmtc._run(argv)

        unexpected_stdout_msg = """Usage: vtmtc.py [FILE]"""
        self.assertNotEqual(unexpected_stdout_msg, stdout_msg)

        # calling the script with 2 arguments, doesn't show help message

        argv = (script_name, 'hello', 'world')

        stdout_msg = vtmtc._run(argv)

        unexpected_stdout_msg = """Usage: vtmtc.py [FILE]"""
        self.assertNotEqual(unexpected_stdout_msg, stdout_msg)

    def test_cancollapsemultilinesrow(self):
        """
        Multi-lines row in vim-table-mode looks like this:

        |-------------------------+----------------------------------|
        | Lorem ipsum dolor       | Suspendisse quis ipsum           |
        | sit amet                | diam. Etiam tristique            |
        |                         | libero et imperdiet tempor.      |
        |-------------------------+----------------------------------|
        | Donec semper augue      | Quisque sodales rutrum           |
        | et metus consequat      | nulla, a pretium dui cursus nec. |
        | lobortis quis ac metus. |                                  |
        |-------------------------+----------------------------------|

        We want to convert it to look like this (single-line row):

        |---------------------------------------------------------------+--------------------------------------------------------------------------|
        | Lorem ipsum dolor sit amet                                    | Suspendisse quis ipsum diam. Etiam tristique libero et imperdiet tempor. |
        |---------------------------------------------------------------+--------------------------------------------------------------------------|
        | Donec semper augue et metus consequat lobortis quis ac metus. | Quisque sodales rutrum nulla, a pretium dui cursus nec.                  |
        |---------------------------------------------------------------+--------------------------------------------------------------------------|
        """

        # simulate file reading with linegen

        multilines_str = """some text

|-------------------------+----------------------------------|
| Lorem ipsum dolor       | Suspendisse quis ipsum           |
| sit amet                | diam. Etiam tristique            |
|                         | libero et imperdiet tempor.      |
|-------------------------+----------------------------------|
| Donec semper augue      | Quisque sodales rutrum           |
| et metus consequat      | nulla, a pretium dui cursus nec. |
| lobortis quis ac metus. |                                  |
|-------------------------+----------------------------------|

some other text"""

        def linegen(multilines):
            for line in multilines.split('\n'):
                yield line

        # for loop can iterate through this variable the same way as
        # when it iterates the result of open()
        multilines_itr = linegen(multilines_str)

        expected_singleline_str = """some text

|---------------------------------------------------------------+---------------------------------------------------------------------------|
| Lorem ipsum dolor sit amet                                    | Suspendisse quis ipsum  diam. Etiam tristique libero et imperdiet tempor. |
|---------------------------------------------------------------+---------------------------------------------------------------------------|
| Donec semper augue et metus consequat lobortis quis ac metus. | Quisque sodales rutrum nulla, a pretium dui cursus nec.                   |
|---------------------------------------------------------------+---------------------------------------------------------------------------|

some other text"""

        result = ''
        for line in vtmtc.collapsemultilines(multilines_itr):
            result += line

        self.assertEqual(result, expected_singleline_str + '\n')

    def test_canconvertvimtablemodetocsv(self):
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
