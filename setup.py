#
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
# esky + bbfreeze setup script
#
from esky import bdist_esky
from distutils.core import setup

setup(
  name = "asmd",
  version = "1.0.0",
  scripts = [
        "asmd.py",
  ],
  options = { "bdist_esky": {
    "includes": []
  }},
)
