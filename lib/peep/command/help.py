# vim: fileencoding=utf-8

CONVMAP = {'\n': '<Return>', ' ': '<Space>'}

class Help(object):

  def __init__(self, desc=''):
    self.desc = desc
    self.contents = []

  def append(self, fn, *keys):
    self.contents.append('%-20s%s'%(' or '.join(map(
      lambda c: CONVMAP.get(c, c), keys)), fn.__doc__))
