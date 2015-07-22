#!/bin/env python

## import
import sys, os

## added library path if not frozen
if not getattr(sys, "frozen", False):
  sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'modules'))
else:
  sys.path.append(os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..', 'modules')))
from asmd_logger import log

## ASMD
class asmd(object):
  """Advanced SmartOS Management Daemon"""

  def __init__(self):
    """Initialized asmd"""
    log("initializing ...")

  def setup(self):
    module_object = getattr(__import__('asmd_config'), 'asmd_config')
    (module_object()).run()

## init
if __name__ == "__main__":
  """initialized asmd based on argv"""
  if '-s' in sys.argv:
    # setup mode, ignore other opts
    asmd().setup()
  elif '-d' in sys.argv:
    # service mode, parse next opt
    pass
  else:
    log('please run asmd via smf or provide -s to run setup.', error=True)
    sys.exit(1)
