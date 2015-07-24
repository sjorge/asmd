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
ASMD_BASE=$(cd $(dirname $0)/..; pwd)
ASMD_SERVICE_METHODE=
ASMD_SERVICE_INSTANCE=

## asmd::core::log
asmd_core_log() {
  printf "[%s] %s\n" "$(date +'%Y/%m/%d %H:%M:%S')" "$*"
}

## asmd::core::setup
asmd_core_setup() {
  # create smf xml
  SMF_XML=$(mktemp)
  cat ${ASMD_BASE}/share/00-asmd_smf.xml.in >> ${SMF_XML}

  # for every service run asmd_service_setup + push xml fragment
  for SERVICE in $(ls ${ASMD_BASE}/services/*.service); do
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
    . ${SERVICE}
    ASMD_SSERVICE_CLASS=$(basename "${SERVICE}")
    ASMD_SSERVICE_CLASS=${ASMD_SSERVICE_CLASS%%.*}

    # skip if force disabled
    [ -e /usbkey/config.inc/.asmd_disable_${ASMD_SSERVICE_CLASS} ] && continue

    # run asmd_service_setup if delcared
    declare -f -F "asmd_service_setup" > /dev/null
    if [ $? -eq 0 ]; then
      asmd_core_log "configuring ${ASMD_SERVICE_NAME} ..."
      asmd_service_setup
    fi

    # push smf instance begin
    printf "    <instance name='%s' enabled='true'>\n" "${ASMD_SERVICE_NAME}" >> ${SMF_XML}

    # push smf dependancies
    DEPI=0
    for DEP in ${ASMD_SERVICE_DEPENDENCIES}; do
      DEPI=$((${DEPI} + 1))
      printf "      <dependency name='%s-dependency-%d' grouping='require_all' restart_on='error' type='service'>\n" \
         ${ASMD_SERVICE_NAME} \
         ${DEPI} \
         >> ${SMF_XML}
      printf "        <service_fmri value='%s'/>\n" \
        "${DEP}" \
        >> ${SMF_XML}
      printf "      </dependency>\n" \
        >> ${SMF_XML}
    done

    DEPI=0
    for DEP in ${ASMD_SERVICE_DEPENDENTS}; do
      DEPI=$((${DEPI} + 1))
      printf "      <dependent name='%s-dependent-%d' grouping='require_all' restart_on='refresh'>\n" \
        "${ASMD_SERVICE_NAME}" \
         ${DEPI} \
         >> ${SMF_XML}
      printf "        <service_fmri value='%s'/>\n" \
        "${DEP}" \
        >> ${SMF_XML}
      printf "      </dependent>\n" \
        >> ${SMF_XML}
    done

     # push smf instance end
     printf "      <exec_method name='start' type='method' exec='%s/bin/asmd -i %s -m start' timeout_seconds='120'/>\n" \
       "${ASMD_BASE}" \
       "${ASMD_SSERVICE_CLASS}" \
       >> ${SMF_XML}
     printf "      <exec_method name='stop' type='method' exec='%s/bin/asmd -i %s -m stop' timeout_seconds='120'/>\n" \
       "${ASMD_BASE}" \
       "${ASMD_SSERVICE_CLASS}" \
       >> ${SMF_XML}
     printf "      <property_group name='startd' type='framework'>\n" >> ${SMF_XML}
     case ${ASMD_SERVICE_TYPE} in
       transient)
         printf "        <propval name='duration' type='astring' value='transient'/>\n" >> ${SMF_XML}
       ;;
     esac
     printf "        <propval name='ignore_error' type='astring' value='core,signal'/>\n" >> ${SMF_XML}
     printf "      </property_group>\n" >> ${SMF_XML}
     printf "      <template>\n" >> ${SMF_XML}
     printf "        <common_name>\n" >> ${SMF_XML}
     printf "          <loctext xml:lang='C'>%s</loctext>\n" "${ASMD_SERVICE_DESC} ">> ${SMF_XML}
     printf "        </common_name>\n" >> ${SMF_XML}
     printf "      </template>\n" >> ${SMF_XML}
     printf "    </instance>\n" >> ${SMF_XML}

  done
  cat ${ASMD_BASE}/share/99-asmd_smf.xml.in >> ${SMF_XML}
  mkdir -p /opt/custom/smf/
  mv ${SMF_XML} /opt/custom/smf/asmd.xml
  asmd_core_log "reboot or run 'svccfg import /opt/custom/smf/asmd.xml' to start asmd."
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
