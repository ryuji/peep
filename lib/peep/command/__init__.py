# vim: fileencoding=utf-8

import keybindings
from message import Message

__all__ = ['execute']

def execute(app, key=None):
  callback = keybindings.get(app.mode, key)
  if callback:
    try:
      callback(app)
    except Message,   m: getattr(app.ui.command_line, m.type)(m)
    except Exception, e: app.ui.command_line.err(e)
