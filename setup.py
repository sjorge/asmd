#
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
# esky + bbfreeze setup script
#
import sys, os
from esky import bdist_esky
from distutils.core import setup
sys.path.append(sys.path[0] + '/modules')

modules = []
for f in os.listdir(sys.path[0]):
  if not os.path.isfile(os.path.join(sys.path[0], 'modules', f)):
    continue
  if f.startswith('asmd_') and f.endswith('.py'):
    modules.append(f[:-3])

setup(
  name = "asmd",
  version = "1.0.0",
  scripts = [
        "asmd.py",
  ],
  options = { "bdist_esky": {
    "includes": modules
  }},
)
