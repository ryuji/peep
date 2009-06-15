# vim: fileencoding=utf-8

from ConfigParser import SafeConfigParser

class Config(SafeConfigParser):

  def __init__(self, files):
    SafeConfigParser.__init__(self)
    self.read(files)
    for x in self.sections(): setattr(self, x, Option(self.items(x)))

  def set(self, section, option, value):
    SafeConfigParser.set(self, section, option, value)
    getattr(self, section)[option] = value

class Option(dict):

  def __getattr__(self, key):
    try:
      return self[key]
    except KeyError, e:
      raise AttributeError(e)
