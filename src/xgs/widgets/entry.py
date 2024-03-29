from xgs.widgets.misc import ShellWidget, Bindable
from xgs.style import info, warn, error

from gi.repository import Gtk

class Entry(Gtk.Entry, ShellWidget):
    def __init__(self, placeholder="", visibility=True, on_accept=None):
        Gtk.Entry.__init__(self, placeholder_text=placeholder, visibility=visibility)
        
        if on_accept is not None and callable(on_accept) is True:
            self.connect("activate", on_accept)
        
        