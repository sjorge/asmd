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

  def run(self, service, methode):
    log("loading service %s ..." % service)

    try:
      module_object = getattr(__import__('asmd_service_%s' % service), 'asmd_service_%s' % service)
      if methode.lower() == 'start':
        (module_object()).start()
      if methode.lower() == 'stop':
        (module_object()).stop()
    except:
      log("failed to load serivce %s!" % service)


## init
if __name__ == "__main__":
  """initialized asmd based on argv"""
  if '-s' in sys.argv:
    # setup mode, ignore other opts
    asmd().setup()
  elif '-d' in sys.argv and '-m' in sys.argv:
    service = sys.argv[(1+sys.argv.index('-d'))]
    methode = sys.argv[(1+sys.argv.index('-m'))]
    asmd().run(service, methode)
  else:
    log('please run asmd via smf or provide -s to run setup.', error=True)
    sys.exit(1)
