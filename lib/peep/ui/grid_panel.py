# vim: fileencoding=utf-8

from peep.const import CONF
from panel import *

class GridPanel(Panel):

  def __init__(self, stdscr):
    Panel.__init__(self, stdscr)

    self.selected = self.scrolled = 0
    self.rows = []
    for i in range(self.height):
      self.rows.append(self.win.subwin(1, self.width, i, 0))

  def clear(self):
    self.rows[self.selected-self.scrolled].bkgd(' ', curses.A_NORMAL)
    self.selected = self.scrolled = 0
    for row in self.rows:
      row.erase()
      row.noutrefresh()
    curses.doupdate()

  def update(self, entries):
    for i,entry in enumerate(entries[self.scrolled:self.height]):
      self.update_row(entry, i)
    self.show()

  def update_row(self, entry, index=None):
    if index == None: index = self.selected-self.scrolled
    row = self.rows[index]
    row.erase()
    if self.selected-self.scrolled == index:
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

  def select(self, entries, new_index):
    old_index = self.selected
    self.selected = new_index
    self.update_row(entries[old_index], old_index-self.scrolled)
    self.update_row(entries[new_index], new_index-self.scrolled)
    curses.doupdate()

  def scroll(self, lines=1):
    self.win.scroll(lines)
    self.win.refresh()
    self.scrolled += lines

  def move(self, end_cond, scroll_cond, entries, lines=1):
    new_index = self.selected+lines
    if end_cond(new_index): return False
    if scroll_cond(new_index): self.scroll(lines)
    self.select(entries, new_index)
    return True

  def next(self, entries):
    return self.move(lambda i: i >= len(entries),
                     lambda i: i-self.scrolled >= self.height,
                     entries)

  def prev(self, entries):
    return self.move(lambda i: i < 0,
                     lambda i: i-self.scrolled < 0,
                     entries, -1)
