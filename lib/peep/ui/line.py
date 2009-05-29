# vim: fileencoding=utf-8

import curses

from component import *

class Line(Component):

  def __init__(self, stdscr, position, attr=curses.A_NORMAL):
    Component.__init__(self, stdscr)

    self.win = stdscr.subwin(1, self.width, self.height+position, 0)
    self.height, self.width = self.win.getmaxyx()

    self.win.bkgd(' ', attr)
    self.win.noutrefresh()
