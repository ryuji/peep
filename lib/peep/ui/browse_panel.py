# vim: fileencoding=utf-8

from subprocess import Popen, PIPE

from panel import *

class BrowsePanel(Panel):

  def __init__(self, stdscr):
    Panel.__init__(self, stdscr)

    self.h_height = 5
    self.header = self.win.subwin(self.h_height, self.width, 0, 0)
    self.b_height = self.height - self.h_height
    self.body = self.win.subpad(self.b_height, self.width, self.h_height, 0)

  def clear(self):
    self.header.erase()
    self.header.refresh()
    self.body.erase()
    self.body.refresh()

  def update(self, entry):
    self.clear()
    self.update_header(entry)
    self.update_body(entry)
    self.show()

  def format_header(self, label, value):
    return U(u'%9s: %s'%(label, value), self.width)

  def update_header(self, entry):
    F = self.format_header
    self.header.addstr(0, 0, F('Feed', entry['subscription_title']))
    self.header.addstr(1, 0, F('Title', entry['title']))
    self.header.addstr(2, 0, F('Published', format_date(entry['published'])))
    self.header.addstr(3, 0, F('Author', entry['author']))
    self.header.addstr(3, self.width-1, u'!' if entry['pinned'] else u' ')
    self.header.hline(4, 0, curses.ACS_HLINE, self.width)
    self.header.noutrefresh()

  def update_body(self, entry):
    cmd = 'w3m -dump -T text/html -cols %d' % self.width
    proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
    proc.stdin.write(entry['content'].encode('utf-8'))
    proc.stdin.close()

    self.content = proc.stdout.readlines()
    self.scrolled = 0
    for i,line in enumerate(self.content[self.scrolled:self.b_height]):
      self.body.addstr(i, 0, line)
    self.body.noutrefresh()
