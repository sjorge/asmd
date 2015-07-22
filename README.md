# Advanced SmartOS Management Daemon
asmd aims to replace a few bash glue services 
 I have for my personal SmartOS nodes.

The following will be implemented:

* admin tag over vnic :: support for the admin tag to be over a vnic
* cron 
* notify helper :: setup sendmail for fowarding

## profile service
Files placed in /usblkey/asmd/profile will be symlinked in 
 /root. E.g. a custom .bashrc and .vimrc.
