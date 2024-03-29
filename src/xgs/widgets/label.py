from xgs.widgets.misc import ShellWidget, Bindable
from xgs.style import warn
from typing import Literal

from gi.repository import Gtk, Gio, Pango, GObject


class Label(Gtk.Label, ShellWidget):
    def __init__(self, label: Bindable | str ="", justification: Literal["center", "fill", "left", "right"]="", 
                 truncate: Literal["end", "middle", "none", "start"]="", xalign=0.5, wrap=False, use_markup=False,
                 **kwargs):
        
        Gtk.Label.__init__(self, ellipsize=getattr(Pango.EllipsizeMode, truncate.upper(), Pango.EllipsizeMode.NONE), 
                           justify=getattr(Gtk.Justification, justification.upper(), Gtk.Justification.CENTER), 
                           xalign=xalign, wrap=wrap, use_markup=use_markup, **kwargs)
        ShellWidget.__init__(self)
        
        if isinstance(label, Bindable) is True:
            self._create_binding(label, self.set_label, str)
        else:
            self.set_label(label)