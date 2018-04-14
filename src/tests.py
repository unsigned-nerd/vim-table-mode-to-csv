#!/usr/bin/env python3

import unittest
import vtmtc

from unittest.mock import MagicMock

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
          Usage: vtmtc.py [IN_FILE] [OUT_FILE]
        """

        script_name = 'vtmtc.py'

        # calling the script without an argument, shows help message

        argv = (script_name, )

        stdout_msg = vtmtc._run(argv)

        expected_stdout_msg = """Usage: vtmtc.py [IN_FILE] [OUT_FILE]"""
        self.assertEqual(expected_stdout_msg, stdout_msg)

        # calling the script with an argument, show help message

        argv = (script_name, 'hello')

        stdout_msg = vtmtc._run(argv)

        unexpected_stdout_msg = \
            """Usage: vtmtc.py [IN_FILE] [OUT_FILE]"""
        self.assertEqual(unexpected_stdout_msg, stdout_msg)

        # calling the script with 2 arguments, doesn't show help message

        argv = (script_name, 'hello', 'world')

        vtmtc.vimtablefiletocsvfile = MagicMock(return_value='')
        stdout_msg = vtmtc._run(argv)

        unexpected_stdout_msg = \
            """Usage: vtmtc.py [IN_FILE] [OUT_FILE]"""
        self.assertNotEqual(unexpected_stdout_msg, stdout_msg)

    def test_callvtmtcforreal(self):
        script_name = 'vtmtc.py'

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

        with open('test/tmp/vimtable.in', 'w') as vimtable_file:
            vimtable_file.write(vimtable_text)

        argv = (script_name, 'test/tmp/vimtable.in', 'test/tmp/vimtable.csv')

        vtmtc._run(argv)

        vimtable_csvfile = open('test/tmp/vimtable.csv')

        csvfile_line_0 = next(vimtable_csvfile).rstrip()
        self.assertEqual(csvfile_line_0, 'Lorem ipsum dolor sit amet,' +
            'Suspendisse diam. Etiam,')
        csvfile_line_1 = next(vimtable_csvfile).rstrip()
        self.assertEqual(csvfile_line_1, 'Donec et metus lobortis,' +
            '"Quisque nulla, a",')

        vimtable_csvfile.close()

        import os
        os.remove('test/tmp/vimtable.in')
        os.remove('test/tmp/vimtable.csv')

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

        line_list = vtmtc.vimtable_to_row_list(vimtable)

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

        line_list = vtmtc.vimtable_to_row_list(vimtable)

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

        line_list = vtmtc.vimtable_to_row_list(vimtable)

        line_list_0 = next(line_list)
        self.assertEqual(line_list_0, expected_result_0)
        line_list_1 = next(line_list)
        self.assertEqual(line_list_1, expected_result_1)

    def test_canconvertvimtablemoderowlisttocsvline(self):
        vimtablemode_row_list = [
            'Lorem ipsum dolor sit amet',
            'Suspendisse diam, etiam'
        ]

        csv_line = vtmtc.vimtable_row_list_to_csv_line(
            vimtablemode_row_list)

        self.assertEqual(csv_line, 'Lorem ipsum dolor sit amet,' +
            '"Suspendisse diam, etiam",')

    def test_canconvertvimtablefiletocsvfile(self):
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

        with open('test/tmp/vimtable.in', 'w') as vimtable_file:
            vimtable_file.write(vimtable_text)

        vtmtc.vimtablefiletocsvfile('test/tmp/vimtable.in',
            'test/tmp/vimtable.csv')

        vimtable_csvfile = open('test/tmp/vimtable.csv')

        csvfile_line_0 = next(vimtable_csvfile).rstrip()
        self.assertEqual(csvfile_line_0, 'Lorem ipsum dolor sit amet,' +
            'Suspendisse diam. Etiam,')
        csvfile_line_1 = next(vimtable_csvfile).rstrip()
        self.assertEqual(csvfile_line_1, 'Donec et metus lobortis,' +
            '"Quisque nulla, a",')

        vimtable_csvfile.close()

        import os
        os.remove('test/tmp/vimtable.in')
        os.remove('test/tmp/vimtable.csv')

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
