# vim: fileencoding=utf-8

import curses

from line import *

class StatusLine(Line):

  def __init__(self, stdscr):
    Line.__init__(self, stdscr, -2, curses.A_REVERSE)

  def update(self, title, pinnedn, staredn, unreadn):
    stats = u' [!:%d][*:%d][U:%d]' % (pinnedn, staredn, unreadn)
    n = self.width - len(stats)
    self.win.addstr(0, 0, U(title, n))
    self.win.insstr(0, n, U(stats, len(stats)))
    self.win.refresh()
