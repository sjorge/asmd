#!/bin/sh
#
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
#
VERSION=1.0.0
[ -d dist/ ] && rm -rf dist/
mkdir -p dist/asmd
mkdir -p dist/asmd/{bin,etc}
cp asmd.sh dist/asmd/bin/asmd
cp -r share dist/asmd/
cp -r services dist/asmd/
tar czvf dist/asmd-${VERSION}.tar.gz -C dist/ asmd/
