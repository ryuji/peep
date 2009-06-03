# vim: fileencoding=utf-8

import curses
import locale

import command
from const import CONF, MODE
from reader import Reader
from ui import MainScreen

class App(object):

  def __setattr__(self, name, value):
    if name == 'mode':
      if not hasattr(self, name):
        object.__setattr__(self, 'prev_mode', value)
      elif getattr(self, name) != value:
        object.__setattr__(self, 'prev_mode', getattr(self, name))
    object.__setattr__(self, name, value)

  def print_unread_count(self):
    print Reader(**CONF.credential).get_unread_count()

  def main(self):
    locale.setlocale(locale.LC_ALL, '')  # anti garbled
    try:
      curses.wrapper(self.event_loop)
    except KeyboardInterrupt:
      # curses.wrapper is not handling KeyboardInterrupt?
      self.stdscr.keypad(0)
      curses.nocbreak()
      curses.echo()
      curses.endwin()

  def event_loop(self, stdscr):
    self.stdscr = stdscr  # need except KeyboardInterrupt
    self.reader = Reader(**CONF.credential)
    self.ui = MainScreen(stdscr)
    command.execute(self) # switch unread mode
    while 1: command.execute(self, stdscr.getkey())
