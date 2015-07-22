#!/bin/sh
#
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
# build an esky package
#
rm -rf dist/
python setup.py sdist
python setup.py bdist
python setup.py bdist_esky
rm -rf asmd.egg-info/ build/
rm dist/*.gz
mkdir -p dist/asmd/bin
unzip dist/asmd-*.zip -d dist/asmd/bin
rm dist/*.zip
cp -r data/share/ dist/asmd/
tar czvf dist/asmd-$(grep version setup.py | awk -F'"' '{ print $2 }').tar.gz -C dist/ asmd/
rm -rf dist/asmd/
