from xgs.widgets.misc import ShellWidget

from gi.repository import Gtk

class Button(Gtk.Button, ShellWidget):
    def __init__(self, child=None, on_clicked=None, on_hover=None, **kwargs):
        Gtk.Button.__init__(self, child=child, on_clicked=on_clicked, on_hover=on_hover, **kwargs)
        ShellWidget.__init__(self)