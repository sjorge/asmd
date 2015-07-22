from asmd_helper import log, smartos_config
import os

class asmd_service_cron(object):
  """asmd cron service :: populate crontab from /usbkey/config"""
  crontab = "/var/spool/cron/crontabs/root"

  def __init__(self):
    """pre-launch stuff for cron service"""
    log("initializing ...", log_name='asmd::service::cron')

  def start(self):
    log("starting ...", log_name='asmd::service::cron')

    log("clearing old crontab entries ...", log_name='asmd::service::cron')
    if os.path.isfile(self.crontab):
      crontab_new = []
      with open(self.crontab, 'r') as crontab:
        for line in crontab:
          line = line.strip()
          if line.endswith("# asmd-cron-entry"):
            continue
          crontab_new.append(line)
      with open(self.crontab, 'w') as crontab:
        for line in crontab_new:
          crontab.write("%s\n" % line)

    log("adding crontab entries ...", log_name='asmd::service::cron')
    config = smartos_config().parse()
    for entry in config:
      if not entry.startswith("cron_"):
        continue
      with open(self.crontab, 'a') as crontab:
        crontab.write("%s # asmd-cron-entry\n" % config[entry].strip())

  def stop(self):
    """daemon stop"""
    pass # not required for transient service

  def smf_instance_config(self):
    config = {}
    config['name'] = "cron-setup"
    config['transient'] = True
    config['description'] = "populate crontab from /usbkey/config"
    config['dependents'] = {}
    config['dependents']['cron'] = "svc:/system/cron:default"
   
    return config
