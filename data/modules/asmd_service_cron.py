from asmd_helper import log, smartos_config
from subprocess import Popen, PIPE
import os, shutil

class asmd_service_cron(object):
  """asmd cron service :: populate crontab from /usbkey/config"""
  crontab = "/var/spool/cron/crontabs/root"
  config = None

  def __init__(self):
    """pre-launch stuff for cron service"""
    log("initializing ...", log_name='asmd::service::cron')
    self.config = smartos_config().parse()

  def start(self):
    log("starting ...", log_name='asmd::service::cron')

    # remove all cron jobs added by asmd
    log("clearing crontab jobs ...", log_name='asmd::service::cron')
    if os.path.isfile(self.crontab):
      with open("%s_asmd" % self.crontab, 'w') as crontab_new:
        with open(self.crontab, 'r') as crontab:
          for line in crontab:
            if '# asmd-cron-job' in line:
              continue # discard, once of ours
            crontab_new.write(line)
      # move work file to final
      shutil.move("%s_asmd" % self.crontab, self.crontab)

    if 'cron' in self.config:
      with open(self.crontab, 'a') as crontab:
        for entry in sorted(self.config['cron']):
          log("adding crontab job [%s] ..." % entry, log_name='asmd::service::cron')
          crontab.write("%s # asmd-cron-job [%s]\n" % (self.config['cron'][entry].strip(), entry))

    # signal crond for crontab update
    log("signaling crond to relaod crontab ...", log_name='asmd::service::cron')
    pgrep_proc = Popen(['/usr/bin/pgrep', 'cron'], stdout=PIPE)
    cron_pid = pgrep_proc.communicate()[0].strip()
    pgrep_proc.wait()
    kill_proc = Popen(['/usr/bin/kill', '-THAW', cron_pid])
    kill_proc.wait()

  def stop(self):
    """stop hook for cron service"""
    log("nothing to stop.", log_name='asmd::service::cron')

  def smf_instance_config(self):
    config = {}
    config['name'] = "cron-setup"
    config['transient'] = True
    config['description'] = "populate crontab from /usbkey/config"
    config['dependencies'] = {}
    config['dependencies']['fs-local'] = "svc:/system/filesystem/local"
    config['dependencies']['cron'] = "svc:/system/cron:default"
   
    return config
