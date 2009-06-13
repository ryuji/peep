# vim: fileencoding=utf-8

class Message(Exception):

  def __init__(self, value, type='inform'):
    self.value, self.type = value, type

  def __unicode__(self):
    return unicode(self.value)
