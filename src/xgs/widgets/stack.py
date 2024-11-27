from xgs.widgets.misc import ShellWidget
from xgs.style import info, warn, error

from typing import Literal
from gi.repository import Gtk

class Stack(Gtk.Stack, ShellWidget):
    def __init__(self, transition_type: Literal["none","crossfade","slide_right",
                                                "slide_left","slide_up","slide_down",
                                                "slide_left_right","slide_up_down","over_up",
                                                "over_down","over_left","over_right","under_up",
                                                "under_down","under_left","under_right","over_up_down",
                                                "over_down_up","over_left_right","over_right_left"] = "none",
                        transition_duration: int= 100,
                        shown: str = "",
                        children: dict[str, Gtk.Widget] = {},
                        **kwargs):
        
        Gtk.Stack.__init__(self, transition_type=getattr(Gtk.StackTransitionType, transition_type.upper()),
                           transition_duration=transition_duration,
                           visible_child=shown)
        
        ShellWidget.__init__(self)
        
        for name, widget in children.items():
            self.add_named(widget, name)
        