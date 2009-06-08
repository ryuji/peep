# vim: fileencoding=utf-8

import os

from config import Config

APP_HOME = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../'))

CONF = Config([
  os.path.join(APP_HOME, 'peeprc'),
  '/etc/peeprc',
  os.path.expanduser('~/.peeprc'),
])

class MODE(object):
  UNREAD  = 0
  BROWSE  = 1
  STARRED = 2
  HELP    = 9
