#!/bin/env python

## import
import sys, os

## added library path if not frozen
if not getattr(sys, "frozen", False):
  sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'modules'))
else:
  sys.path.append(os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..', 'modules')))
from asmd_helper import log

## ASMD
class asmd(object):
  """Advanced SmartOS Management Daemon"""

  def __init__(self):
    """Initialized asmd"""
    log("initializing ...", log_name='asmd::core')

  def setup(self):
    module_object = getattr(__import__('asmd_config'), 'asmd_config')
    (module_object()).run()

  def run(self, service, methode):
    try:
      module_object = getattr(__import__('asmd_service_%s' % service), 'asmd_service_%s' % service)
      if methode.lower() == 'start':
        (module_object()).start()
      if methode.lower() == 'stop':
        (module_object()).stop()
    except Exception, e:
      log("error in %s module: %s" % (service, e), error=True, log_name='asmd::core')
      sys.exit(95)

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
    log('please run asmd via smf or provide -s to run setup.', error=True, log_name='asmd::loader')
    sys.exit(99)
