from asmd_helper import log
import os, sys

class asmd_config(object):
  """asmd configuration helper"""
  smf_path = "/opt/custom/smf"
  smf_file = "asmd.xml"
  asmd_base = None
  _error = False

  def __init__(self):
    """initialized configuration helper"""
    if not getattr(sys, "frozen", False):
      self.asmd_base = os.path.dirname(sys.argv[0])
    else:
      self.asmd_base = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..'))

  def _getInstanceCfgs(self):
    """retrieve service instance cfg"""
    smf_instances = []
    for service in os.listdir(os.path.join(self.asmd_base, 'modules')):
      # check we are dealing with a asmd_service_*.py file
      if not os.path.isfile(os.path.join(self.asmd_base, 'modules', service)):
        continue
      if not service.startswith("asmd_service_") or not service.endswith(".py"):
        continue

      # extract service name
      service_class = service[:-3]
      service_name = service[len("asmd_service_"):-3]
      log("discovered service %s." % service_name, log_name='asmd::config')

      try:
        module_object = getattr(__import__(service_class), service_class)
        cfg_data = (module_object()).smf_instance_config()
        if 'name' not in cfg_data:
          cfg_data['name'] = service_name
        cfg_data['service'] = service_name
        smf_instances.append(cfg_data)
      except Exception, e:
        log("error in %s module: %s" % (service, e), error=True, log_name='asmd::config')
        self._error = True
 
    return smf_instances

  def run(self):
    """setup asmd"""
    log("initializing ...", log_name='asmd::config')
    if not os.path.isdir(self.smf_path):
      log("creating %s ..." % self.smf_path, log_name='asmd::config')
      os.makedirs(self.smf_path, 755) 

    log("creating service manifest ...", log_name='asmd::config')
    with open(os.path.join(self.smf_path, self.smf_file), 'w') as smf: 
      # load xml templates
      smf_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf.xml.in')).read()
      smf_instance_transient_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf_transient.xml.in')).read().rstrip()
      smf_instance_daemon_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf_daemon.xml.in')).read().rstrip()
      smf_instance_dependency_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf_dependency.xml.in')).read().rstrip()
      smf_instance_dependent_xml = open(os.path.join(self.asmd_base, 'share', 'asmd_smf_dependent.xml.in')).read().rstrip()

      # generate instance xml fragments
      smf_instance_data = []
      for cfg in self._getInstanceCfgs():
        # select correct template (transient or daemon)
        xml = smf_instance_transient_xml if cfg['transient'] else smf_instance_daemon_xml

        # generate dependency xml fragments
        service_deps = []
        if 'dependencies' in cfg:
          for name in cfg['dependencies']:
            service_deps.append(smf_instance_dependency_xml.format(name=name, svc=cfg['dependencies'][name]))
        if 'dependents' in cfg:
          for name in cfg['dependents']:
            service_deps.append(smf_instance_dependent_xml.format(name=name, svc=cfg['dependents'][name]))
          
        # append xml fragment to array
        smf_instance_data.append(xml.format(
          description=cfg['description'],
          name=cfg['name'], 
          service=cfg['service'], 
          dependencies="\n".join(service_deps),
          ASMD_BIN=sys.argv[0]
        ))

      # write xml fragments to file
      smf.write(smf_xml.format(instances="\n".join(smf_instance_data)))
      log("done! reboot or run 'svccfg import %s' to enable." % os.path.join(self.smf_path, self.smf_file), log_name='asmd::config')
      sys.exit(97 if self._error else 0)
