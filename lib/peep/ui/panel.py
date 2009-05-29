# vim: fileencoding=utf-8

import curses
import curses.panel

from component import *

class Panel(Component):

  def __init__(self, stdscr):
    Component.__init__(self, stdscr)

    self.win = curses.newwin(self.height-2, self.width, 0, 0)
    self.panel = curses.panel.new_panel(self.win)
    self.height, self.width = self.win.getmaxyx()

    self.win.scrollok(True)

  def show(self):
    top = curses.panel.top_panel()
    if not top.hidden(): top.hide()

    self.panel.top()
    self.panel.show()

    curses.panel.update_panels()
    curses.doupdate()
