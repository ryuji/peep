# vim: fileencoding=utf-8

import curses
import locale

import command
from config import Config
from const import CONF_FILES, MODE
from reader import Reader
from ui import MainScreen

class App(object):

  def __init__(self):
    self.conf = Config(CONF_FILES)
    self.reader = Reader(**self.conf.credential)

  def __setattr__(self, name, value):
    if name == 'mode':
      if not hasattr(self, name):
        object.__setattr__(self, 'prev_mode', value)
      elif getattr(self, name) != value:
        object.__setattr__(self, 'prev_mode', getattr(self, name))
    object.__setattr__(self, name, value)

  def print_unread_count(self):
    print self.reader.get_unread_count()

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
    self.ui = MainScreen(stdscr)
    self.mode = MODE.UNREAD
    while 1: command.execute(self, stdscr.getkey())
