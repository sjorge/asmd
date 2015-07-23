#!/usr/bin/bash
####
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
# asmd::core
####

## load smartos helpers
. /lib/svc/share/smf_include.sh
. /lib/sdc/config.sh
 
load_sdc_sysinfo
load_sdc_config

## asmd environment
ASMD_BASE=$(dirname $0)/..
ASMD_SERVICE_METHODE=
ASMD_SERVICE_INSTANCE=

## asmd::core::log
asmd_core_log() {
  printf "[%s] %s\n" "$(date +'%Y/%m/%d %H:%M:%S')" "$*"
}

## asmd::core::setup
asmd_core_setup() {
  # for every service run asmd_service_setup
  for service in $(ls ${ASMD_BASE}/services/*.service); do
    # reset service variables
    ASMD_SERVICE_NAME=
    ASMD_SERVICE_DESC=
    ASMD_SERVICE_TYPE=
    ASMD_SERVICE_DEPENDENCIES=
    ASMD_SERVICE_DEPENDENTS=
    unset -f asmd_service_start
    unset -f asmd_service_stop
    unset -f asmd_service_setup

    # source service variables
    . ${service}

    # run asmd_service_setup if delcared
    declare -f -F "asmd_service_setup" > /dev/null
    if [ $? -eq 0 ]; then
      asmd_core_log "configuring ${ASMD_SERVICE_NAME} ..."
      asmd_service_setup
    fi
  done
}

## asmd::core:::service
asmd_core_service() {
  METHODE=$1
  INSTANCE=$2
  asmd_core_log "loading ${INSTANCE} .."
  . ${ASMD_BASE}/services/${INSTANCE}.service
  declare -f -F "asmd_service_${METHODE}" > /dev/null
  [ $? -gt 0 ] && asmd_core_log "${ASMD_SERVICE_INSTANCE} missing asmd_service_${METHODE}" && exit ${SMF_EXIT_ERR_FATAL}
  eval asmd_service_${METHODE}
}

## asmd::core
# parse opts
while [[ $# > 0 ]]; do
  key="$1"

  case $key in
    -s|--setup)
      asmd_core_setup
      exit ${SMF_EXIT_OK} # we are done here
    ;;
    -m|--methode)
      ASMD_SERVICE_METHODE=${2,,}
      shift
    ;;
    -i|--instance)
      ASMD_SERVICE_INSTANCE=${2,,}
      shift
    ;;
    *) ;;
  esac
  shift
done

# validate opts
[ -z ${ASMD_SERVICE_METHODE} ] && \
  asmd_core_usage && exit ${SMF_EXIT_ERR_NOSMF}
[ -z ${ASMD_SERVICE_INSTANCE} ] && \
  asmd_core_usage && exit ${SMF_EXIT_ERR_NOSMF}
[ ! -e ${ASMD_BASE}/services/${ASMD_SERVICE_INSTANCE}.service ] && \
  asmd_core_log "service [${ASMD_SERVICE_INSTANCE}] does not exist!" && exit ${SMF_EXIT_ERR_NOSMF}

# execute methode
case ${ASMD_SERVICE_METHODE} in
  start|stop)
    asmd_core_service ${ASMD_SERVICE_METHODE} ${ASMD_SERVICE_INSTANCE}  
  ;;
  restart|refresh)
    asmd_core_service stop ${ASMD_SERVICE_INSTANCE}  
    sleep 3
    asmd_core_service start ${ASMD_SERVICE_INSTANCE}  
  ;;
  *)
    asmd_core_log "unknow methode: ${ASMD_SERVICE_METHODE}!" 
    exit ${SMF_EXIT_ERR_NOSMF}
  ;;
esac
exit ${SMF_EXIT_OK}
