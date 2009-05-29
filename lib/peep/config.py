# vim: fileencoding=utf-8

from ConfigParser import SafeConfigParser

class Config(object):

  def __init__(self, files):
    cp = SafeConfigParser()
    cp.read(files)
    for x in cp.sections(): setattr(self, x, Option(cp.items(x)))

class Option(dict):

  def __getattr__(self, key):
    try:
      return self[key]
    except KeyError, e:
      raise AttributeError, e
