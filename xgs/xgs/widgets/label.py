from xgs.widgets.misc import ShellWidget, Bindable

from typing import Literal

from gi.repository import Gtk, Gio, Pango


class Label(Gtk.Label, ShellWidget):
    def __init__(self, label: Bindable | str ="", justification: Literal["center", "fill", "left", "right"]="", 
                 truncate: Literal["end", "middle", "none", "start"]="", xalign=0.5, wrap=False, use_markup=False):
        
        Gtk.Label.__init__(self, ellipsize=getattr(Pango.EllipsizeMode, truncate.upper(), Pango.EllipsizeMode.NONE), 
                           justify=getattr(Gtk.Justification, justification.upper(), Gtk.Justification.CENTER), 
                           xalign=xalign, wrap=wrap, use_markup=use_markup)
        ShellWidget.__init__(self)
        
        if isinstance(label, Bindable) is True:
            self.bind_property("label", label, label.bindable_prop_name, transform_to=label.bindable_transform_func)
        else:
            self.set_label(label)
        
        ShellWidget.__init__(self)