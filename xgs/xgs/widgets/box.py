from gi.repository import Gtk
from xgs.services.binding import Bindable

class Box(Gtk.Box, Bindable):
    def __init__(self, spacing=0, vertical=False, children=[], homogeneous=False, **kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL if not vertical else Gtk.Orientation.VERTICAL,
                         spacing=spacing,
                         homogeneous=homogeneous,
                         **kwargs)
        Bindable.__init__(self)
        self.appends(*children)

    def appends(self, *args):
        for x in args:
            self.append(x)
