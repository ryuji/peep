# vim: fileencoding=utf-8

from optparse import OptionParser
import sys

from app import App

__version__   = '1.0-beta-1'
__copyright__ = 'Copyright (c) 2009 Ryuji Matsumura <ryuji@mgiken.com>'
__license__   = 'GPL 3.0'

def main(argv=sys.argv):
  # parse arguments
  parser = OptionParser(version='%prog '+__version__)
  parser.add_option('-n', '--notify', action='store_true', dest='notify',
                    help='notify unread entry count')
  opts, args = parser.parse_args()

  # main routine
  try:
    if len(argv) == 1:
      App().main()
    elif opts.notify:
      App().print_unread_count()
    else:
      parser.print_help()
  except Exception, e:
    sys.exit(e)
