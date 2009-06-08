# vim: fileencoding=utf-8

class Message(Exception):

  def __init__(self, message, type='inform'):
    self.message, self.type = message, type

  def __str__(self):
    return self.message
