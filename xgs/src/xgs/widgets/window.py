from gi.repository import Gtk, Gdk, GObject, GLib
from gi.repository import Gtk4LayerShell as LayerShell

from xgs.utils import GArray
from xgs.style import info, debug, error, warn
from xgs.widgets.misc import ShellWidget

from typing import Literal, List

def get_monitor(gdk_display: Gdk.Display, mon_id):
    mon_vec = gdk_display.get_monitors()
    return mon_vec.get_item(mon_id)

class Window(Gtk.Window, ShellWidget):
    app=None
    def __init__(self, name, layer: Literal["top", "bottom", "overlay", "background"]="top", 
                 child=None, monitor=0, anchor: List[Literal["top", "right", "bottom", "left"]]=[], margins=[], className="", width=0, 
                 height=0, exclusive=True):
        
        Gtk.Window.__init__(self, application=Window.app)
        ShellWidget.__init__(self)

        self.set_default_size(width, height) 
        self.set_css_name(className)

        LayerShell.init_for_window(self)
        LayerShell.set_layer(self, getattr(LayerShell.Layer, layer.upper()))
        LayerShell.set_namespace(self, name)

        self.monitor = monitor
        self.anchor = anchor
        self.exclusive = exclusive

        self.set_monitor(self.monitor)
        self.set_anchor(self.anchor)
        self.set_exclusive(self.exclusive)
        
        if child is not None:
            self.set_child(child)

        if margins != []:
            self.set_margins(margins)

        info(f'Showing window {name}...')
        self.present()

    def name(self):
        """
        Returns the name of the window, if self.get_name is a empty string or None, returns unknown.
        """
        return 'unknown' if not (n:=Gtk.Window.get_name(self)) else n
   
    def set_monitor(self, mon_id):
        debug(f"Setting monitor on window {self.get_name()}...")

        mon = Gdk.Display.get_default()
        if mon is not None:
            LayerShell.set_monitor(self, get_monitor(mon, mon_id))
            self._monitor = mon_id
   
    def set_anchor(self, anchors: list[str]): 
        debug("Setting anchors")
        length = len(anchors)
        if length > 4:
            anchors = anchors[:3]
        for anchor in anchors:
            anchor_obj = getattr(LayerShell.Edge, anchor.upper())
            if anchor_obj is not None:
                LayerShell.set_anchor(self, anchor_obj, True) 
            else:
                print(f"invalid anchor: '{anchor}'")
        self._anchor = GArray()
        self._anchor.list = anchors
   
    def set_exclusive(self, exclusive):
        debug("Setting exclusive")
        if exclusive is True:
            LayerShell.auto_exclusive_zone_enable(self)
        else:
            LayerShell.set_exclusive_zone(self, 0)
