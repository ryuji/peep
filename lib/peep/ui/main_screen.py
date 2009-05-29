# vim: fileencoding=utf-8

import curses
import curses.panel

#from browse_panel import BrowsePanel
from command_line import CommandLine
from grid_panel  import GridPanel
from status_line import StatusLine
from component import Component

class MainScreen(Component):

  def __init__(self, stdscr):
    Component.__init__(self, stdscr)

    try:
      curses.curs_set(0)  # hide cursor if possible
    except:
      pass  # ignore exception

    # init colors
    if curses.has_colors():
      curses.use_default_colors()
      curses.init_pair(1, curses.COLOR_RED, -1)
      curses.init_pair(2, curses.COLOR_YELLOW, -1)

    # init screen
#    self.browse_panel = BrowsePanel(stdscr)
    self.grid_panel = GridPanel(stdscr)
    self.status_line = StatusLine(stdscr)
    self.command_line = CommandLine(stdscr)

    # refresh
    curses.panel.update_panels()
    curses.doupdate()
