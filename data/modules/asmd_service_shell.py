from asmd_logger import log
import os
class asmd_service_shell(object):
  """asmd shell service :: setup /root's home"""

  def start(self):
    log("service::shell starting ...")

  def stop(self):
    log("service::shell stopping ...")

  def smf_instance_config(self):
    config = {}
    config['transient'] = True
    config['description'] = "Setup /root's home"
    config['dependencies'] = {}
    config['dependencies']['fs-local'] = "svc:/system/filesystem/local"
   
    return config
