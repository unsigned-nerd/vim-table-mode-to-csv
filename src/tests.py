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

    # when a script is called without any argument from a shell,
    # sys.argv is an empty tuple
    args = tuple()

    stdout_msg = vtmtc._run(args)

    expected_stdout_msg = """Usage: vtmtc.py [FILE]\n"""
    self.assertEqual(expected_stdout_msg, stdout_msg)

if __name__ == '__main__':
    unittest.main()
