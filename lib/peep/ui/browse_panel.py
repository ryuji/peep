# vim: fileencoding=utf-8

from subprocess import Popen, PIPE

from panel import *

class BrowsePanel(Panel):

  def __init__(self, stdscr):
    Panel.__init__(self, stdscr)

    self.scrolled = 0
    self.h_height = 5
    self.header = self.win.subwin(self.h_height, self.width, 0, 0)
    self.b_height = self.height - self.h_height
    self.body = self.win.subwin(self.b_height, self.width, self.h_height, 0)
    self.body.scrollok(True)

  def update(self, entry):
    self.scrolled = 0
    self.update_header(entry)
    self.update_body(entry)
    self.show()

  def format_header(self, label, value):
    return U(u'%9s: %s'%(label, value), self.width)

  def update_header(self, entry):
    self.header.erase()

    F = self.format_header
    self.header.addstr(0, 0, F('Feed', entry['subscription_title']))
    self.header.addstr(1, 0, F('Title', entry['title']))
    self.header.addstr(2, 0, F('Published', format_date(entry['published'])))
    self.header.addstr(3, 0, F('Author', entry['author']))
    self.header.addstr(3, self.width-1, u'!' if entry['pinned'] else u' ')
    self.header.hline(4, 0, curses.ACS_HLINE, self.width)
    self.header.noutrefresh()

  def update_body(self, entry):
    self.body.erase()

    if not entry.get('converted'):
      cmd = 'w3m -dump -T text/html -cols %d' % (self.width-2)
      proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
      proc.stdin.write(entry['content'].encode('utf-8'))
      proc.stdin.close()
      entry['content'] = proc.stdout.readlines()
      entry['converted'] = True

    content = entry['content'][self.scrolled:self.b_height+self.scrolled-1]
    for i,line in enumerate(content): self.body.addstr(i, 0, line)
    self.body.noutrefresh()

  def move(self, end_cond, entry, range, way=1):
    scrolled = self.scrolled + (range*way if range else self.b_height*way)
    if end_cond(scrolled+(self.b_height if range else 1)): return
    self.scrolled = scrolled
    if self.scrolled < 0: self.scrolled = 0
    self.update_body(entry)
    self.body.refresh()

  def up(self, entry, range=None):
    self.move(lambda i: self.scrolled == 0, entry, range, -1)

  def down(self, entry, range=None):
    self.move(lambda i: i >= len(entry['content']), entry, range)
