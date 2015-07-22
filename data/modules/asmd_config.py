from asmd_logger import log
import os, sys
class asmd_config(object):
  """asmd configuration helper"""
  smf_path = "/opt/custom/smf"
  smf_file = "asmd.xml"
  asmd_base = None

  def __init__(self):
    """initialized configuration helper"""
    if not getattr(sys, "frozen", False):
      self.asmd_base = os.path.dirname(sys.argv[0])
    else:
      self.asmd_base = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..'))

  def run(self):
    """setup asmd"""

    log("initializing ...", log_name='asmd::config')
    if not os.path.isdir(self.smf_path):
      log("creating %s ..." % self.smf_path, log_name='asmd::config')
      os.makedirs(self.smf_path, 755) 

    log("creating service manifest ...", log_name='asmd::config')
    with open(os.path.join(self.smf_path, self.smf_file), 'w') as smf: 
      smf_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf.xml.in')).read()
      smf_instance_transient_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf_transient.xml.in')).read()
      smf_instance_daemon_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf_daemon.xml.in')).read()
      smf_instance_dependency_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf_dependency.xml.in')).read()

      smf_instances = []
      for service in os.listdir(os.path.join(self.asmd_base, 'modules')):
        if not os.path.isfile(os.path.join(self.asmd_base, 'modules', service)):
          continue
        if not service.startswith("asmd_service_"):
          continue
        service_class = service[:-3]
        service_name = service[len("asmd_service_"):-3]
        log("discovered service %s." % service_name, log_name='asmd::config')

        module_object = getattr(__import__(service_class), service_class)
        cfg_data = (module_object()).smf_instance_config()
        if 'name' not in cfg_data:
          cfg_data['name'] = service_name
        cfg_data['service'] = service_name
        smf_instances.append(cfg_data)
   
      smf_instance_data = []
      for cfg in smf_instances:
        xml = smf_instance_transient_xml if cfg['transient'] else smf_instance_daemon_xml
        service_deps = []
        for name in cfg['dependencies']:
          dep_xml = smf_instance_dependency_xml
          service_deps.append(dep_xml.format(name=name, svc=cfg['dependencies'][name]))
          
        smf_instance_data.append(xml.format(
          description=cfg['description'],
          name=cfg['name'], 
          service=cfg['service'], 
          dependencies="\n".join(service_deps),
          ASMD_BIN=sys.argv[0]
        ))

      smf.write(smf_xml.format(instances="\n".join(smf_instance_data)))
      log("done! reboot or run 'svccfg import %s' to enable." % os.path.join(self.smf_path, self.smf_file), log_name='asmd::config')
