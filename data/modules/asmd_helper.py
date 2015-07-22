import sys, time, os, errno

class log(object):
  """logging module"""

  def __init__(self, msg, color='', error=False, raw=False, log_name='asmd'):
    """colorful logging function"""
    COLOR_DGRAY  = '\033[90m'
    COLOR_RED    = '\033[91m'
    COLOR_GREEN  = '\033[92m'
    COLOR_YELLOW = '\033[93m'
    COLOR_BLUE   = '\033[94m'
    COLOR_PINK   = '\033[95m'
    COLOR_CYAN   = '\033[96m'
    COLOR_WHITE  = '\033[97m'
    COLOR_LGRAY  = '\033[98m'
    COLOR_RESET  = '\033[0m'

    TEXT_COLOR = COLOR_LGRAY
    if color.lower() == 'red':
      TEXT_COLOR = COLOR_RED
    elif color.lower() == 'green':
      TEXT_COLOR = COLOR_GREEN
    elif color.lower() == 'blue':
      TEXT_COLOR = COLOR_BLUE
    elif color.lower() == 'yellow':
      TEXT_COLOR = COLOR_YELLOW
    elif color.lower() == 'PINK' or color.lower() == 'MAGENTA':
      TEXT_COLOR = COLOR_PINK
    elif color.lower() == 'cyan':
      TEXT_COLOR = COLOR_CYAN
    elif color.lower() == 'white':
      TEXT_COLOR = COLOR_WHITE
    elif color.lower() == 'gray' or color.lower() == 'grey':
      TEXT_COLOR = COLOR_LGRAY
    elif color.lower() == 'black':
      TEXT_COLOR = COLOR_DGRAY

    log = sys.stderr if error else sys.stdout
    if not raw:
      log.write(
        '\r%s%s%s %s%s%s: %s%s%s\n' % (
          COLOR_DGRAY,
          time.strftime('[%Y/%m/%d %H:%M:%S]'),
          COLOR_RESET,
          COLOR_BLUE,
          log_name,
          COLOR_RESET,
          TEXT_COLOR,
          msg,
          COLOR_RESET
        )
      )
    else:
      log.write(
        '\r%s%s%s\n' % (
          TEXT_COLOR,
          msg,
          COLOR_RESET
        )
      )
    log.flush()

class symlink(object):
  """symlink module"""

  def __init__(self, src, dst, force=False):
    """symlink supporting force"""
    try:
        os.symlink(file1, file2)
    except OSError, e:
        if e.errno == errno.EEXIST and force:
            os.remove(file2)
            os.symlink(file1, file2)
            return True
        return False
    finally:
      return True