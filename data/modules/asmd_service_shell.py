from asmd_logger import log
import os
class asmd_service_shell(object):
  """asmd shell service :: setup /root's home"""

  def start(self):
    log("service::shell starting ...")
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
