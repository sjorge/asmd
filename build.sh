#!/bin/sh
####
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
# packaging script
####
VERSION=1.0.0
[ -d dist/ ] && rm -rf dist/
mkdir -p dist/asmd/{bin,etc}
cp bin/asmd.sh dist/asmd/bin/asmd
cp bin/asmd-setup.sh dist/asmd/bin/asmd-setup
find dist/asmd/bin/ -type f -exec chmod +x {} \;
cp -r share dist/asmd/
cp -r services dist/asmd/
pfexec chown -R root:root dist/asmd/
pfexec chmod +x dist/asmd/share/examples/exec/*
tar czpvf dist/asmd-${VERSION}.tar.gz -C dist/ asmd/
