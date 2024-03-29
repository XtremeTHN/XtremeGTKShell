from gi.repository import Gtk
from xgs.widgets.misc import ShellWidget

class Box(Gtk.Box, ShellWidget):
    def __init__(self, spacing=0, vertical=False, children=[], homogeneous=False, **kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL if not vertical else Gtk.Orientation.VERTICAL,
                         spacing=spacing,
                         homogeneous=homogeneous,
                         **kwargs)
        ShellWidget.__init__(self)
        
        
        self.appends(*children)

    def appends(self, *args):
        for x in args:
            self.append(x)
