# vim: fileencoding=utf-8

from keybindings import switch_unread_mode
from decorator import KEYBINDS
from message import Message

__all__ = ['execute']

def execute(app, key=None):
  callback = KEYBINDS.get(app.mode).get(key) if key else switch_unread_mode
  if callback:
    try:
      callback(app)
    except Message,   m: getattr(app.ui.command_line, m.type)(m)
    except Exception, e: app.ui.command_line.err(e)
