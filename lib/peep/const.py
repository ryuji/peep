# vim: fileencoding=utf-8

import os
import re

from config import Config

APP_HOME = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../'))

CONF = Config([
  os.path.join(APP_HOME, 'peeprc'),
  '/etc/peeprc',
  os.path.expanduser('~/.peeprc'),
])

# XXX
CONF.ad_filter.enable = CONF.ad_filter.enable == 'True'
CONF.ad_filter.pattern = re.compile(CONF.ad_filter.pattern)

class MODE(object):
  UNREAD  = 0
  BROWSE  = 1
  STARRED = 2
  HELP    = 9
