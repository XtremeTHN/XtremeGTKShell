from gi.repository import Gtk, GObject, GLib
from xgs.widgets.misc import ShellWidget
from xgs.utils import GArray

class Box(Gtk.Box, ShellWidget):
    def __init__(self, spacing=0, vertical=False, children=[], homogeneous=False, **kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL if not vertical else Gtk.Orientation.VERTICAL,
                         spacing=spacing,
                         homogeneous=homogeneous,
                         **kwargs)
        ShellWidget.__init__(self)
        
        self.__children = []
        
        self.appends(*children)

    def appends(self, *args):
        for x in args:
            self.__children.append(x)
            self.append(x)
            
    @GObject.Property
    def children(self):
        return self.__children

    @children.setter
    def children(self, children: list[Gtk.Widget]):
        if len(self.__children) > 0:
            for x in self.__children:
                self.remove(x)
                
        self.__children = children
        self.appends(children)