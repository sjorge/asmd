from asmd_logger import log
import os
class asmd_service_shell(object):
  """asmd shell service :: setup /root's home"""
  shell_config_dir = "/usbkey/asmd/shell"

  def __init__(self):
    """pre-launch stuff for shell service"""
    log("initializing ...", log_name='asmd::service::shell')

    if not os.path.isdir(self.shell_config_dir):
      log("creating data directory %s ..." % self.shell_config_dir, log_name='asmd::service::shell')
      os.makedirs(self.shell_config_dir)

  def start(self):
    log("starting ...", log_name='asmd::service::shell')
    # TODO: implement me

  def stop(self):
    """daemon stop"""
    pass # not required for transient service

  def smf_instance_config(self):
    config = {}
    config['transient'] = True
    config['description'] = "Setup /root's home"
    config['dependencies'] = {}
    config['dependencies']['fs-local'] = "svc:/system/filesystem/local"
   
    return config
