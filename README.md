# Advanced SmartOS Management Daemon
asmd aims to replace a few bash glue services 
 I have for my personal SmartOS nodes.

## how to install
```
curl http://pkg.blackdot.be/extras/asmd-1.0.1.tar.gz | gzip -d | tar xvpf - -C /opt
/opt/asmd/bin/asmd-setup
```

# Available services
## hostname service
Configures hostname and/or domain name.
### /usbkey/config example for hostname service
```
## hostname
asmd_hostname=scn0
asmd_hostname_domain=example.org
```

## profile service
Files placed in /usbkey/config.inc/profile will be symlinked in 
 /root. E.g. a custom .bashrc and .vimrc.

## exec service
Files placed in /usbkey/config.inc/exec will be executed.

## ipv6 service
**admin_ip6** is now part of upstream SmartOS, leaving service in asmd for a while for legacy setups.

## swap service
Configure additional swap devices, optionally remove the default one.
Useful when you zones is on SSD only and you have a spindle backed pool also available.
### /usbkey/config example for swap service
!! **asmd_swap_additional** takes a space seperated list
```
## swap
# disable zones/swap zvol
asmd_swap_zones=False
# add additional swap devices
asmd_swap_additional="data/swap /root/swapfile"
```

## cron service
Inserts cron jobs in the root crontab.
### /usbkey/config example for cron service
!! use "" around the crontab entries and * needs to be escaped!
```
## crontab
# monitor for faults
asmd_cron_0="0 10,20 \* \* \* /usr/sbin/fmadm faulty"
asmd_cron_1="5 10,20 \* \* \* /usr/sbin/zpool status -x | grep -v 'healthy'"
# zpool scrub
asmd_cron_2="0 2 \* \* 1 /usr/sbin/zpool scrub zones"
```

## mail service
Configure a (smart)relay, with optionally authenticaton.
Also alows for mails to root to be forwarded. Useful if your cron jobs give output.
### /usbkey/config example for mail service
```
asmd_mail_admin=monitoring@example.org
asmd_mail_relay=smtp.example.org
#asmd_mail_domain=example.org
#asmd_mail_auth_user=exampleuser
#asmd_mail_auth_pass=examplepass
```
