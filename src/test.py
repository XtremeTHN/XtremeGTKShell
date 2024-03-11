from xgs.widgets.window import Window

import gi
gi.require_version("Adw","1")
from gi.repository import Gtk, Adw

Adw.init()

def TopBarWindow():
    main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    
    window_title = Gtk.Label(label="kitty")
    main.append(window_title)
    return Window("test", main, "top", anchor=['top','left','right'])

TopBarWindow()
