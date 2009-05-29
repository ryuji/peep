# vim: fileencoding=utf-8

from peep.const import CONF
from panel import *

class GridPanel(Panel):

  def __init__(self, stdscr):
    Panel.__init__(self, stdscr)

    self.selected = 0
    self.scroll = 0
    self.rows = []
    for i in range(self.height):
      self.rows.append(self.win.subwin(1, self.width, i, 0))

  def clear(self):
    self.rows[self.selected].bkgd(' ', curses.A_NORMAL)
    self.selected = 0
    for row in self.rows:
      row.erase()
      row.noutrefresh()

  def update(self, entries):
    for i, entry in enumerate(entries):
      if i < self.height: self.update_row(i, entry)
    self.show()

  def update_row(self, index, entry):
    row = self.rows[index]
    if self.selected-self.scroll == index:
      row.bkgd(' ', curses.A_REVERSE)
    else:
      row.bkgd(' ', curses.A_NORMAL)

    published = format_date(entry['published'],'%m-%d %H:%M')
    n = len(published)
    x = 0
    x = self.update_column(row, x, '!' if entry['pinned'] else ' ', 1)
    x = self.update_column(row, x, '*' if entry['stared'] else ' ', 1)
    x = self.update_column(row, x, 'U' if entry['unread'] else ' ', 1, 1)
    x = self.update_column(row, x, entry['subscription_title'], self.width/5, 2)
    x = self.update_column(row, x, entry['title'], self.width-x-n-2)
    row.insstr(0, self.width-n, published)

    row.move(0, self.width-1)
    row.noutrefresh()

  def update_column(self, row, x, value='', width=-1, space=0):
    if width == -1: width = len(value)
    row.addstr(0, x, U(value, width))
    return x+width+space

  def next(self, entries):
    if self.selected == len(entries)-1: return False

    old_index, new_index = self.selected, self.selected+1
    # scroll down
    if new_index >= self.height:
      self.win.scroll()
      self.win.refresh()
      self.scroll += 1
    # update selected row
    self.selected = new_index
    self.update_row(old_index-self.scroll, entries[old_index])
    self.update_row(new_index-self.scroll, entries[new_index])
    curses.doupdate()

    return True

  def prev(self, entries):
    if self.selected == 0: return False

    old_index, new_index = self.selected, self.selected-1
    # scroll up
    if new_index-self.scroll < 0:
      self.win.scroll(-1)
      self.win.refresh()
      self.scroll -= 1
    # update selected row
    self.selected = new_index
    self.update_row(old_index-self.scroll, entries[old_index])
    self.update_row(new_index-self.scroll, entries[new_index])
    curses.doupdate()

    return True
