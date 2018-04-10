#!/usr/bin/env python3

import subprocess
import unittest

class TestCommandLineUsage(unittest.TestCase):

  def setUp(self):
    pass
  
  def tearDown(self):
    pass

  def test_callwithoutarg(self):
    """
    If call our script without any argument, shows help message.  Like
    this:

      $ vtmtc.py
      Usage: vtmtc.py [FILE]
    """

    expected_help_msg = """Usage: vtmtc.py [FILE]\n"""

    res = subprocess.run(["./vtmtc.py"], stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)
    
    # subprocess.CompletedProcess.stdout is a bytes sequence, we need to
    # decode it into a string before comparing them with
    # self.assertEqual
    output = res.stdout.decode('utf8')

    self.assertEqual(expected_help_msg, output)

if __name__ == '__main__':
    unittest.main()
