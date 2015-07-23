from asmd_helper import log, smartos_config
from subprocess import Popen, PIPE
import os

class asmd_service_swap(object):
  """asmd swap service :: manage swap"""
  config = None

  def __init__(self):
    """pre-launch stuff for swap service"""
    log("initializing ...", log_name='asmd::service::swap')
    self.config = smartos_config().parse()

  def _getSwapDevs(self):
    """return active swap devices"""
    swap = []
    swap_proc = Popen(['/usr/sbin/swap', '-l'], stdout=PIPE, stderr=PIPE)
    for swapdev in swap_proc.stdout:
      swapdev = swapdev.strip()
      if swapdev.startswith('swapfile'):
        continue # skip header
      if swapdev == "No swap devices configured":
        continue # skip of no devices
      swapdev = [sd for sd in swapdev.split(" ") if sd] 
      swap.append(swapdev[0].strip())
    swap_proc.wait()
    return swap

  def _addSwapDev(self, swapdev):
    """add a swapdev if not present"""
    if not swapdev in self._getSwapDevs():
      swap_proc = Popen(['/usr/sbin/swap', '-a', swapdev])
      swap_proc.wait()

  def _rmSwapDev(self, swapdev):
    """remove swapdev if present"""
    if swapdev in self._getSwapDevs():
      swap_proc = Popen(['/usr/sbin/swap', '-d', swapdev])
      swap_proc.wait()

  def _getSwapSummary(self):
    """return swap summary"""
    swap_proc = Popen(['/usr/sbin/swap', '-s', '-h'], stdout=PIPE)
    summary = swap_proc.communicate()[0].strip()
    swap_proc.wait()
    return summary

  def start(self):
    """enable additional swap devices"""
    log("starting ...", log_name='asmd::service::swap')
    
    # no config, do nothing
    if not 'swap' in self.config:
      log("nothing to do.", log_name='asmd::service::swap')
      pass

    # add aditional swap devices
    for swapdev in self.config['swap']:
      # skip if additional device
      if not swapdev.startswith('additional_'):
        continue 

      # get swapdev path
      swapdev = self.config['swap'][swapdev].strip()
      if not swapdev[0] == '/': # assume zvol
        swapdev = "/dev/zvol/dsk/%s" % swapdev

      # check if it exists before adding
      if os.path.exists(swapdev):
        log("adding %s" % swapdev, log_name='asmd::service::swap')
        self._addSwapDev(swapdev)
      else:
        log("missing swap device %s" % swapdev, error=True, log_name='asmd::service::swap')

    # remove zones/swap if needed
    if 'zones' in self.config['swap'] and self.config['swap']['zones'].lower() in [ 'false', 'no', 'disabled' ]:
      log("removing /dev/zvol/dsk/zones/swap", log_name='asmd::service::swap')
      self._rmSwapDev("/dev/zvol/dsk/zones/swap")

    # log swap summary
    log(self._getSwapSummary(), log_name='asmd::service::swap')

  def stop(self):
    """disable additional swap devices"""
    log("stopping ...", log_name='asmd::service::swap')
    
    # add zones/swap
    if os.path.exists("/dev/zvol/dsk/zones/swap"):
      log("adding /dev/zvol/dsk/zones/swap", log_name='asmd::service::swap')
      self._addSwapDev("/dev/zvol/dsk/zones/swap")

    # remove aditional swap devices
    for swapdev in self._getSwapDevs():
      if swapdev == "/dev/zvol/dsk/zones/swap":
        continue # skip zones/swap
      log("removing %s" % swapdev, log_name='asmd::service::swap')
      self._rmSwapDev(swapdev)

    # log swap summary
    log(self._getSwapSummary(), log_name='asmd::service::swap')

  def smf_instance_config(self):
    config = {}
    config['name'] = "swap-setup"
    config['transient'] = True
    config['description'] = "manage additional swap devices from /usbkey/config"
    config['dependents'] = {}
    config['dependents']['zones'] = "svc:/system/zones:default"
   
    return config
