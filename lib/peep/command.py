# vim: fileencoding=utf-8

import sys
import webbrowser

from const import CONF, MODE

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

def update_status(fn):
  def wrapper(app):
    fn(app)
    # TODO
    app.ui.status_line.update(app.reader.get_feed_title(),
                              app.reader.get_pinned_count(),
                              0,
                              app.reader.get_unread_count())
  return wrapper

# callback functions ---------------------------------------------------------

@callback(MODE.UNREAD, 'q')
@confirm(u'Are you sure you want to quit?')
def quit(app):
  sys.exit()

@callback(MODE.BROWSE, 'q')
def back(app):
  switch_unread_mode(app)

@callback(MODE.UNREAD, 'r')
def refresh(app):
  app.reader.clear_cache()
  app.ui.grid_panel.clear()
  switch_unread_mode(app)

@callback(MODE.BROWSE, 'u')
@loading
@update_status
def switch_unread_mode(app):
  app.mode = MODE.UNREAD
  app.ui.grid_panel.update(app.reader.get_unread_entries())

@callback(MODE.UNREAD, '\n')
@loading
@update_status
def switch_browse_mode(app):
  app.mode = MODE.BROWSE
  entry = get_selected_entry(app)
  app.ui.browse_panel.update(entry)
  app.reader.set_read(entry)

@callback(MODE.UNREAD, 'j')
def next(app):
  return app.ui.grid_panel.next(app.reader.get_unread_entries())

@callback(MODE.UNREAD, 'k')
def prev(app):
  return app.ui.grid_panel.prev(app.reader.get_unread_entries())

@callback(MODE.BROWSE, 'j')
def next_browse(app):
  if next(app): switch_browse_mode(app)

@callback(MODE.BROWSE, 'k')
def prev_browse(app):
  if prev(app): switch_browse_mode(app)

@callback(MODE.BROWSE, ' ')
def down(app):
  app.ui.browse_panel.down(get_selected_entry(app))

@callback(MODE.BROWSE, '\n')
@callback(MODE.BROWSE, 'J')
def down1(app):
  app.ui.browse_panel.down(get_selected_entry(app), 1)

@callback(MODE.BROWSE, '-')
def up(app):
  app.ui.browse_panel.up(get_selected_entry(app))

@callback(MODE.BROWSE, 'K')
def up1(app):
  app.ui.browse_panel.up(get_selected_entry(app), 1)

@callback(MODE.UNREAD, 'm')
@callback(MODE.BROWSE, 'm')
@update_status
def toggle_read(app):
  entry = get_selected_entry(app)
  app.reader.toggle_read(entry)
  update_panel(app, entry)

@callback(MODE.UNREAD, 'p')
@callback(MODE.BROWSE, 'p')
@update_status
def toggle_pin(app):
  entry = get_selected_entry(app)
  app.reader.toggle_pin(entry)
  update_panel(app, entry)

@callback(MODE.UNREAD, 'O')
@callback(MODE.BROWSE, 'O')
@update_status
def open(app):
  entry = get_selected_entry(app)
  open_external_browser(app, entry)
  update_panel(app, entry)

@callback(MODE.UNREAD, 'o')
@callback(MODE.BROWSE, 'o')
@update_status
def open_pinned_entries(app):
  for i in range(int(CONF.browse.max_count)):
    if app.reader.get_pinned_count() == 0: break
    entry = app.reader.get_pinned_entries().pop(0)
    open_external_browser(app, entry)
    entry['pinned'] = False
  if app.mode == MODE.BROWSE:
    app.ui.browse_panel.update_header(get_selected_entry(app))
  else:
    app.ui.grid_panel.update(app.reader.get_unread_entries())

# helper functions -----------------------------------------------------------

def get_selected_entry(app):
  return app.reader.get_unread_entries()[app.ui.grid_panel.selected]

def update_panel(app, entry):
  if app.mode == MODE.BROWSE: app.ui.browse_panel.update_header(entry)
  else:                       app.ui.grid_panel.update_row(entry)

def open_external_browser(app, entry):
  try:
    webbrowser.open_new_tab(entry['link'])
    app.reader.set_read(entry)
  except:
    raise Exception(u'Failed to open external web browser')
