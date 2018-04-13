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

    def test_canconvertvimtableintolist(self):
        """
        vim-table with multi-line rows looks like this:

            |-------------------+-------------|
            | Lorem ipsum dolor | Suspendisse |
            | sit amet          | diam. Etiam |
            |-------------------+-------------|
            | Donec             | Quisque     |
            | et metus          | nulla, a    |
            | lobortis          |             |
            |-------------------+-------------|

        We want to create a generator which takes the input above and
        yields lists that looks like this:

           #0 ['Lorem ipsum dolor sit amet', 'Suspendisse diam. Etiam']
           #1 ['Donec et metus lobortis', 'Quisque nulla, a']
        """

        # test 0

        vimtable_text = """some text

            |-------------------+-------------|
            | Lorem ipsum dolor | Suspendisse |
            | sit amet          | diam. Etiam |
            |-------------------+-------------|
            | Donec             | Quisque     |
            | et metus          | nulla, a    |
            | lobortis          |             |
            |-------------------+-------------|

            some other text"""

        # simulate open() BIF, this way, we don't have to create a real
        # dummy file for testing
        vimtable = (line for line in vimtable_text.split('\n'))

        expected_result_0 = ['Lorem ipsum dolor sit amet',
            'Suspendisse diam. Etiam']
        expected_result_1 = ['Donec et metus lobortis',
            'Quisque nulla, a']

        line_list = vtmtc.vimtable_to_line_list(vimtable)

        line_list_0 = next(line_list)
        self.assertEqual(line_list_0, expected_result_0)
        line_list_1 = next(line_list)
        self.assertEqual(line_list_1, expected_result_1)

        # test 1

        vimtable_text = """some text

            |-------------------+-------------|
            | Lorem ipsum dolor |             |
            | sit amet          | diam. Etiam |
            |-------------------+-------------|
            | Donec             | Quisque     |
            | et metus          | nulla, a    |
            | lobortis          |             |
            |-------------------+-------------|

            some other text"""

        # simulate open() BIF, this way, we don't have to create a real
        # dummy file for testing
        vimtable = (line for line in vimtable_text.split('\n'))

        expected_result_0 = ['Lorem ipsum dolor sit amet',
            'diam. Etiam']
        expected_result_1 = ['Donec et metus lobortis',
            'Quisque nulla, a']

        line_list = vtmtc.vimtable_to_line_list(vimtable)

        line_list_0 = next(line_list)
        self.assertEqual(line_list_0, expected_result_0)
        line_list_1 = next(line_list)
        self.assertEqual(line_list_1, expected_result_1)

        # test 2

        vimtable_text = """some text

            |----------+----------|
            |          |          |
            |          |          |
            |----------+----------|
            | Donec    | Quisque  |
            | et metus | nulla, a |
            | lobortis |          |
            |----------+----------|

            some other text"""

        # simulate open() BIF, this way, we don't have to create a real
        # dummy file for testing
        vimtable = (line for line in vimtable_text.split('\n'))

        expected_result_0 = ['', '']
        expected_result_1 = ['Donec et metus lobortis',
            'Quisque nulla, a']

        line_list = vtmtc.vimtable_to_line_list(vimtable)

        line_list_0 = next(line_list)
        self.assertEqual(line_list_0, expected_result_0)
        line_list_1 = next(line_list)
        self.assertEqual(line_list_1, expected_result_1)


        self.fail('Finish the test!')

    def test_canconvertvimtablemodetocsv(self):
        pass

if __name__ == '__main__':
    unittest.main()
