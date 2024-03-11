import gi
gi.require_versions({'Gtk':'4.0', 'Gtk4LayerShell': '1.0'})

from gi.repository import Gtk, Gdk, GObject, GLib
from gi.repository import Gtk4LayerShell as LayerShell

from xgs.utils import GArray

def get_monitor(gdk_display: Gdk.Display, mon_id):
    mon_vec = gdk_display.get_monitors()
    return mon_vec.get_item(mon_id)

class Window(Gtk.Window):
    app=None
    def __init__(self, name, child: Gtk.Widget, layer: str, monitor=0, anchor=[], className="", width=0, height=0, exclusive=True):
        super().__init__(application=Window.app)
        
        self.set_default_size(width, height) 

        LayerShell.init_for_window(self)
        LayerShell.set_layer(self, getattr(LayerShell.Layer, layer.upper()))
        LayerShell.set_namespace(self, name)

        self.monitor = monitor
        self.anchor = anchor
        self.exclusive = exclusive

        self.set_monitor(self.monitor)
        self.set_anchor(self.anchor)
        self.set_exclusive(self.exclusive)

        self.set_child(child)

        print('presenting')
        self.present()
    
   
    def set_monitor(self, mon_id):
        print("setting mon")
        mon = Gdk.Display.get_default()
        if mon is not None:
            LayerShell.set_monitor(self, get_monitor(mon, mon_id))
            self._monitor = mon_id
   
    def set_anchor(self, anchors: list[str]): 
        print("setting anchors")
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
        print("setting exclusive")
        if exclusive is True:
            LayerShell.auto_exclusive_zone_enable(self)
        else:
            LayerShell.set_exclusive_zone(self, 0)

def set_margins(widget: Gtk.Widget, margins: list[int]):
    """
        Reminder: margins = [top, right, bottom, left]
    """
    length = len(margins)
    
    top = margins[0]
    right = margins[1] if length > 1 else top
    bottom = margins[2] if length > 2 else right
    left = margins[3] if length > 3 else bottom

    widget.set_margin_top(top)
    widget.set_margin_end(right)
    widget.set_margin_bottom(bottom)
    widget.set_margin_start(left)

