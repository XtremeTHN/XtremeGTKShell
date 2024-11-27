from xgs.widgets.misc import ShellWidget

from gi.repository import Gtk

class Button(Gtk.Button, ShellWidget):
    def __init__(self, child=None, on_clicked=None, **kwargs):
        Gtk.Button.__init__(self, child=child, **kwargs)
        ShellWidget.__init__(self)
        
        if on_clicked is not None:
            self.connect("clicked", on_clicked)