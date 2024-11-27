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
                
        self.appends(*children)

    def appends(self, *args):
        for x in args:
            self.append(x)
            
    @GObject.Property
    def children(self):
        return None

    @children.setter
    def children(self, children: list[Gtk.Widget]):
        self.clear()
        self.appends(children)
    
    def clear(self):
        """Removes all children from the box
        Does nothing if theres no child to be removed
        """
        # C Implementation for removing all childs of a box. From https://discourse.gnome.org/t/delete-all-children-from-a-gtkbox-in-gtk4/8279/3
        childs = self.get_first_child()
        while childs:
            self.remove(childs)
            childs = self.get_first_child()