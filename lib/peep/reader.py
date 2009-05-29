# vim: fileencoding=utf-8

from GoogleReader import GoogleReader, CONST

class Reader(object):

  def __init__(self, email, password):
    self.reader = GoogleReader()
    self.reader.identify(email, password)
    if not self.reader.login():
      raise Exception(u'Failed to login to Google Reader')
