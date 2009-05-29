# vim: fileencoding=utf-8

from datetime import datetime
import unicodedata

# W - East Asian Wide
# F - East Asian Fullwidth
# A - East Asian Ambiguous
# see also <http://www.unicode.org/reports/tr11/>
WIDE_CHARS = u'WFA'

def U(s, n=0):
  if not isinstance(s, unicode): s = unicode(s)
  if n <= 0: return s.encode('utf-8')
  u, i = u'', 0
  for c in s:
    i += 1 if WIDE_CHARS.find(unicodedata.east_asian_width(c))<0 else 2
    if i > n: break
    u += c
  return u.encode('utf-8')

def format_date(timestamp, format='%Y-%m-%d %H:%M'):
  return datetime.fromtimestamp(timestamp).strftime(format)

class Component(object):

  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.height, self.width = stdscr.getmaxyx()
