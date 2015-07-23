from asmd_helper import log, symlink
import os

class asmd_service_profile(object):
  """asmd profile service :: setup /root's home"""
  profile_config_dir = "/usbkey/asmd/profile"

  def __init__(self):
    """pre-launch stuff for profile service"""
    log("initializing ...", log_name='asmd::service::profile')

    # create config_dir if missing
    if not os.path.isdir(self.profile_config_dir):
      log("creating data directory %s ..." % self.profile_config_dir, log_name='asmd::service::profile')
      os.makedirs(self.profile_config_dir)

  def start(self):
    log("starting ...", log_name='asmd::service::profile')
    for f in os.listdir(self.profile_config_dir):
      # create symlink for each file under /root
      symlink().link(
        os.path.join(self.profile_config_dir, f),
        os.path.join('/root', f),
        force=True
      )
      log("linking %s" % os.path.join('/root', f), log_name='asmd::service::profile')

  def smf_instance_config(self):
    config = {}
    config['name'] = "profile-setup"
    config['transient'] = True
    config['description'] = "Setup /root's home"
    config['dependencies'] = {}
    config['dependencies']['fs-local'] = "svc:/system/filesystem/local"
   
    return config
