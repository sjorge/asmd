#!/usr/bin/bash
####
# Advanced SmartOS Management Daemon
# 2015 By Jorge Schrauwen
# ----------------------------------
# exec script example - vnic
# :: removed the smartos configured
#    ipv4 address and sets up dual
#    stack addresses over a vnic
#    configured with an vlan
#    e.g. useful over an aggr with 
#    only tagged vlans
####

##
# this example exec scripts uses the smartos
#  config parser and include some helpers 
#  from the ipv6 service.
#
# it consume the following aditional 
#  /usbkey/config variables to set
#  a fixed mac for the vnic and 
#  specify the vlan id to use
#  otherwise it reuses the native
#  and ipv6 address variables.
#  the vnic is create over the 
#  admin_nic tag.
# 
# admin_vnic_mac=00:15:00:xx:yy:zz
# admin_vnic_vlan=30
##

## load smartos config parser
. /lib/sdc/config.sh
 
load_sdc_sysinfo
load_sdc_config
 
## load asmd helper (replace /opt/local with your PREFIX)
. /opt/local/asmd/share/helpers/ipv6/validate.sh
. /opt/local/asmd/share/helpers/ipv6/update_hosts.sh
 
## lookup admin nic
NIC=$(sysinfo -p | grep NIC_admin | awk -F"'" '{ print $2 }')
 
## delete addres smartos configured addresses
ipadm delete-if ${NIC}
 
## create vnic (asmd0) and set addresses
dladm create-vnic -t -l ${NIC} -v ${CONFIG_admin_vnic_vlan} -m ${CONFIG_admin_vnic_mac} asmd0
ipadm create-addr -t -T static -a ${CONFIG_admin_ip}/$(mask2cidr ${CONFIG_admin_netmask}) asmd0/v4s
ipadm create-addr -t -T addrconf asmd0/v6a
ipadm create-addr -t -T static -a ${CONFIG_admin_ip6}/${CONFIG_admin_netmask6} asmd0/v6s

## add default routes after short delay
sleep 2
[ ! -z ${CONFIG_admin_gateway} ] && route add default ${CONFIG_admin_gateway}
[ ! -z ${CONFIG_admin_gateway6} ] &&route add -inet6 default ${CONFIG_admin_gateway6}
 
## give addrconf some time to settle and update /etc/hosts
sleep 5
update_hosts
