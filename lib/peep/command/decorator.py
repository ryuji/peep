# vim: fileencoding=utf-8

from help import Help
from message import Message
from peep.const import MODE

__all__ = ['bindkey', 'confirm', 'loading', 'update_status']

KEYBINDINGS = {
  MODE.UNREAD:  {},
  MODE.BROWSE:  {},
  MODE.STARRED: {},
  MODE.HELP:    {},
}

HELPS = {
  MODE.UNREAD:  Help(u'The Unread Items'),
  MODE.BROWSE:  Help(u'The Pager'),
  MODE.STARRED: Help(u'The Starred Items'),
  MODE.HELP:    Help(),
}

def bindkey(mode, *keys):
  def decorator(fn):
    HELPS[mode].append(fn, *keys)
    for key in keys: KEYBINDINGS[mode][key] = fn
    return fn
  return decorator

def confirm(message, defans=True):
  def decorator(fn):
    def wrapper(app):
      app.ui.command_line.confirm(message, lambda: fn(app), defans)
    wrapper.__doc__ = fn.__doc__
    return wrapper
  return decorator

def loading(fn):
  def wrapper(app):
    app.ui.command_line.loading(lambda: fn(app))
  wrapper.__doc__ = fn.__doc__
  return wrapper

def update_status(fn):
  def wrapper(app):
    try:
      fn(app)
    except Exception, e:
      raise e
    finally:
    # TODO
      app.ui.status_line.update(app.reader.get_feed_title(),
                                app.reader.get_pinned_count(),
                                0,
                                app.reader.get_unread_count())
  wrapper.__doc__ = fn.__doc__
  return wrapper
