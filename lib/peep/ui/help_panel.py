# vim: fileencoding=utf-8

from panel import *

class HelpPanel(Panel):

  def __init__(self, stdscr):
    Panel.__init__(self, stdscr)

  def update(self, help):
    self.win.erase()
    self.win.addstr(0, 0, help.desc)
    self.win.addstr(1, 0, '-'*len(help.desc))
    i = 2
    for x in help.contents:
      self.win.addstr(i, 0, x)
      i += 1
    self.win.refresh()
    self.show()
