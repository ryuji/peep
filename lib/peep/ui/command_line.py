# vim: fileencoding=utf-8

import curses

from line import *

class CommandLine(Line):

  def __init__(self, stdscr):
    Line.__init__(self, stdscr, -1)

  def clear(self):
    self.win.erase()
    self.win.refresh()

  def inform(self, message='', attr=curses.A_NORMAL):
    self.win.erase()
    self.win.bkgd(' ', attr)
    self.win.addstr(0, 0, U(message, self.width))
    self.win.refresh()

  def warn(self, message):
    self.inform(message, curses.color_pair(2))

  def err(self, message):
    curses.beep()
    self.inform(message, curses.color_pair(1))

  def command(self, message, callback):
    # FIXME
    pass

  def confirm(self, message, callback, defans=True):
    self.inform(message+(' (Y/n)' if defans else ' (y/N)'))
    while 1:
      ans = self.stdscr.getkey().lower()
      if ans == '\n': ans = 'y' if defans else 'n'
      if ans == 'y':
        callback()
        break;
      elif ans == 'n':
        break;
    self.clear()

  def loading(self, callback):
    self.inform(u'Loading...')
    callback()
    self.clear()
