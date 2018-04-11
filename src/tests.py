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
    If user calls our script without any argument, shows help message.
    Like this:

      $ vtmtc.py
      Usage: vtmtc.py [FILE]
    """

    # calling the script without an argument, shows help message

    argv = tuple()

    stdout_msg = vtmtc._run(argv)

    expected_stdout_msg = """Usage: vtmtc.py [FILE]\n"""
    self.assertEqual(expected_stdout_msg, stdout_msg)

    # calling the script with an argument, doesn't show help message

    argv = ('hello')

    stdout_msg = vtmtc._run(argv)

    unexpected_stdout_msg = """Usage: vtmtc.py [FILE]\n"""
    self.assertNotEqual(unexpected_stdout_msg, stdout_msg)

    # calling the script with 2 arguments, doesn't show help message

    argv = ('hello', 'world')

    stdout_msg = vtmtc._run(argv)

    unexpected_stdout_msg = """Usage: vtmtc.py [FILE]\n"""
    self.assertNotEqual(unexpected_stdout_msg, stdout_msg)

    self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
