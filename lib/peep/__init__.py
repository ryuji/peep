# vim: fileencoding=utf-8

from getpass import getpass
from optparse import OptionParser
import os
import stat
import sys

from app import App
from const import CONF
from reader import Reader

__version__   = '1.0-beta-1'
__copyright__ = 'Copyright (c) 2009 Ryuji Matsumura <ryuji@mgiken.com>'
__license__   = 'GPL 3.0'

def parse_args():
  parser = OptionParser(version='%prog '+__version__)
  parser.add_option('-n', '--notify', action='store_true', dest='notify',
                    help='notify unread entry count')
  return parser.parse_args()

def init():
  conf_file = os.path.expanduser('~/.peeprc')
  if os.path.exists(conf_file): return

  email = password = ''
  while 1:
    print 'Sign in to Google Reader with your'
    try:
      email, password = raw_input('Email: '), getpass('Password: ')
      Reader(email, password)
    except (EOFError, KeyboardInterrupt):
      sys.exit()
    except Exception, e:
      print '\nThe username or password you entered is incorrect.\n'
    else:
      CONF.set('credential', 'email', email)
      CONF.set('credential', 'password', password)
      CONF.write(file(conf_file, 'w'))
      os.chmod(conf_file, stat.S_IREAD|stat.S_IWRITE)
      break

def main(argv=sys.argv):
  init()
  opts, args = parse_args()
  try:
    if len(argv) == 1: App().main()
    elif opts.notify:  App().print_unread_count()
    else:              parser.print_help()
  except Exception, e:
    sys.exit(e)
