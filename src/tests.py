#!/usr/bin/env python3

import unittest
import vtmtc

from unittest.mock import MagicMock

class MyUnitTest(unittest.TestCase):

    def test_helpmsg(self):
        """
        If user calls our script without any argument or incorrect
        number of expected arguments, shows a help message.  Like this:

          $ vtmtc.py
          Usage: vtmtc.py [IN_FILE] [OUT_FILE]
        """

        # sys.argv[0] is the script name
        script_name = 'vtmtc.py'

        # calling the script without an argument, show help message

        argv = (script_name, )

        stdout_msg = vtmtc._run(argv)

        expected_stdout_msg = """Usage: vtmtc.py [IN_FILE] [OUT_FILE]"""
        self.assertEqual(expected_stdout_msg, stdout_msg)

        # calling the script with an argument, show help message

        argv = (script_name, 'hello')

        stdout_msg = vtmtc._run(argv)

        expected_stdout_msg = \
            """Usage: vtmtc.py [IN_FILE] [OUT_FILE]"""
        self.assertEqual(expected_stdout_msg, stdout_msg)

        # calling the script with 2 arguments, do not show help message

        argv = (script_name, 'hello', 'world')

        original_vimtablefiletocsvfile = vtmtc.vimtablefiletocsvfile
        vtmtc.vimtablefiletocsvfile = MagicMock(return_value='')
        stdout_msg = vtmtc._run(argv)
        vtmtc.vimtablefiletocsvfile = original_vimtablefiletocsvfile

        unexpected_stdout_msg = \
            """Usage: vtmtc.py [IN_FILE] [OUT_FILE]"""
        self.assertNotEqual(unexpected_stdout_msg, stdout_msg)

    def test_canconvertvimtablefiletocsvfile(self):
        """
        test by calling the (nearly) top-level script (via vtmtc._run)
        as we know that vtmtc._run calls vtmtc.vimtablefiletocsvfile, so
        we don't need a dedicated test case for it
        """

        # sys.argv[0] is the script name
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

        argv = (script_name, 'test/tmp/vimtable.in',
            'test/tmp/vimtable.csv')

        vtmtc._run(argv)

        with open('test/tmp/vimtable.csv') as csv_file:
            csv_file_line_0 = next(csv_file)
            self.assertEqual(csv_file_line_0, 'Lorem ipsum dolor sit amet,' +
                'Suspendisse diam. Etiam,\n')
            csv_file_line_1 = next(csv_file).rstrip()
            self.assertEqual(csv_file_line_1, 'Donec et metus lobortis,' +
                '"Quisque nulla, a",')

        # clean up files generated during this test
        import os
        os.remove('test/tmp/vimtable.in')
        os.remove('test/tmp/vimtable.csv')

    def test_canconvertvimtableintocollist(self):
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

        We want to create a generator which takes the input that looks
        like the table above and yields list of columns that looks like
        this per each iteration:

            the first call to next gives:

              ['Lorem ipsum dolor sit amet', 'Suspendisse diam. Etiam']

            the second call to next gives:

              ['Donec et metus lobortis', 'Quisque nulla, a']
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

        line_list = vtmtc.vimtable_to_col_list(vimtable)

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

        line_list = vtmtc.vimtable_to_col_list(vimtable)

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

        line_list = vtmtc.vimtable_to_col_list(vimtable)

        line_list_0 = next(line_list)
        self.assertEqual(line_list_0, expected_result_0)
        line_list_1 = next(line_list)
        self.assertEqual(line_list_1, expected_result_1)

    def test_canconvertvimtablemodecollisttocsvline(self):
        vimtablemode_col_list = [
            'Lorem ipsum dolor sit amet',
            'Suspendisse diam, etiam'
        ]

        csv_line = vtmtc.vimtable_col_list_to_csv_line(
            vimtablemode_col_list)

        self.assertEqual(csv_line, 'Lorem ipsum dolor sit amet,' +
            '"Suspendisse diam, etiam",')

if __name__ == '__main__':
    unittest.main()
