# vim: fileencoding=utf-8

import sys

from const import MODE

CALLBACKS = {
  MODE.UNREAD: {},
  MODE.BROWSE: {},
  MODE.STARED: {},
}

def execute(app, key):
  callback = CALLBACKS.get(app.mode).get(key)
  if callback:
    try:
      callback(app)
    except Exception, e:
      app.ui.command_line.err(e.message)

# decorator functions --------------------------------------------------------

def callback(mode, key):
  def decorator(fn):
    CALLBACKS[mode][key] = fn
    return fn
  return decorator

def confirm(message, defans=True):
  def decorator(fn):
    def wrapper(app):
      app.ui.command_line.confirm(message, lambda: fn(app), defans)
    return wrapper
  return decorator

def loading(fn):
  def wrapper(app):
    app.ui.command_line.loading(lambda: fn(app))
  return wrapper

# callback functions ---------------------------------------------------------

@callback(MODE.UNREAD, 'q')
@confirm(u'Are you sure you want to quit?')
def quit(app):
  sys.exit()
