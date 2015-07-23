from asmd_helper import log, smartos_config
from subprocess import Popen, PIPE
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
          if '# asmd-cron-entry' in line:
            continue
          crontab_new.append(line)
      with open(self.crontab, 'w') as crontab:
        for line in crontab_new:
          crontab.write("%s\n" % line)

    config = smartos_config().parse()
    if 'cron' in config:
      with open(self.crontab, 'a') as crontab:
        for entry in sorted(config['cron']):
          log("adding crontab entry [%s] ..." % entry, log_name='asmd::service::cron')
          crontab.write("%s # asmd-cron-entry [%s]\n" % (config['cron'][entry].strip(), entry))

    log("signaling cron daemon to reload ...", log_name='asmd::service::cron')
    pgrep_proc = Popen(['/usr/bin/pgrep', 'cron'], stdout=PIPE)
    cron_pid = pgrep_proc.communicate()[0].strip()
    pgrep_proc.wait()
    kill_proc = Popen(['/usr/bin/kill', '-THAW', cron_pid])
    kill_proc.wait()

  def stop(self):
    """daemon stop"""
    pass # not required for transient service

  def smf_instance_config(self):
    config = {}
    config['name'] = "cron-setup"
    config['transient'] = True
    config['description'] = "populate crontab from /usbkey/config"
    config['dependencies'] = {}
    config['dependencies']['fs-local'] = "svc:/system/filesystem/local"
    config['dependencies']['cron'] = "svc:/system/cron:default"
   
    return config
