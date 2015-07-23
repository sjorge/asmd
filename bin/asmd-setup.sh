#!/usr/bin/bash
####
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
# asmd::setup wrapper
####

ASMD_BASE=$(dirname $0)/..
[ ! -e ${ASMD_BASE}/bin/asmd ] && exit 1
${ASMD_BASE}/bin/asmd -s
