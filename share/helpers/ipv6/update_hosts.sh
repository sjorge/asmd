update_hosts() {
  HOST_TEMP=$(mktemp)
  head -n26 /etc/hosts > ${HOST_TEMP}
  sleep 5 # give addrconf time to settle
  for IP in $(ipadm show-addr | grep -v lo0 | awk '{ print $NF }' | awk -F'/' '{ print $1 }'); do
    asmd_core_log "updating /etc/hosts for ${IP} ..."
    if [ -z "$(domainname)" ]; then
      echo "${IP}\t$(hostname)" >> ${HOST_TEMP}
    else
      echo -e  "${IP}\t$(hostname).$(domainname) $(hostname)" >> ${HOST_TEMP}
    fi
  done
  mv ${HOST_TEMP} /etc/hosts
}
