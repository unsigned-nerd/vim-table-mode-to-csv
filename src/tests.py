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

    def test_canreadvimtableintolist(self):
        """
        Multi-lines row in vim-table-mode looks like this:

        |-------------------+-------------|
        | Lorem ipsum dolor | Suspendisse |
        | sit amet          | diam. Etiam |
        |-------------------+-------------|
        | Donec             | Quisque     |
        | et metus          | nulla, a    |
        | lobortis          |             |
        |-------------------+-------------|

        We want to read it into a list like this:

           [['Lorem ipsum dolor sit amet', 'Suspendisse diam. Etiam'],
            ['Donec et metus lobortis', 'Quisque nulla, a']]
        """

        # simulate file reading with linegen

        input_text = """some text

|-------------------+-------------|
| Lorem ipsum dolor | Suspendisse |
| sit amet          | diam. Etiam |
|-------------------+-------------|
| Donec             | Quisque     |
| et metus          | nulla, a    |
| lobortis          |             |
|-------------------+-------------|

some other text"""


        # for loop can iterate through this variable the same way as
        # when it iterates the result of open()
        input_itr = (line for line in input_text.split('\n'))

        expected_result = [
            ['Lorem ipsum dolor sit amet', 'Suspendisse diam. Etiam'],
            ['Donec et metus lobortis', 'Quisque nulla, a']]

        result = vtmtc.vimtabletolist(input_itr)

        self.assertEqual(result, expected_result)
        self.fail('Finish the test!')

    def test_canconvertvimtablemodetocsv(self):
        pass

if __name__ == '__main__':
    unittest.main()
