#!/usr/bin/env python3

import sys

def _run(*argv):
  """
  When calling this script from a command line shell, the top level code
  passes all the work to this function so that we can write a test
  easier for command line application.

  This function returns an output string which is to be printed to
  STDOUT by the top level code.
  """

  pass

if __name__ == '__main__':
  print(_run(sys.argv))
