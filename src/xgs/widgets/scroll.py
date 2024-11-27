from xgs.services.binding import Bindable
from xgs.widgets.misc import ShellWidget
from xgs.widgets.box import Box
from xgs.style import warn, info
from gi.repository import Gtk

from typing import Literal

class Scrollable(Gtk.ScrolledWindow, ShellWidget):
    def __init__(self, vscroll: Literal["automatic", "always", "external", "never", "minimum", "natural"] = "automatic", 
                 hscroll: Literal["automatic", "always", "external", "never", "minimum", "natural"]="automatic", 
                 child=None, **kwargs):
        Gtk.ScrolledWindow.__init__(self, child=child, **kwargs)
        ShellWidget.__init__(self)
        # super().__init__(child=child, **kwargs)

        vscroll_mode = getattr(Gtk.PolicyType, vscroll.upper(), "")
        hscroll_mode = getattr(Gtk.PolicyType, hscroll.upper(), "")

        if vscroll_mode == "":
            self.set_property('vscrollbar-policy', Gtk.PolicyType.AUTOMATIC)
            warn(f'Invalid scroll mode "{vscroll}" for vertical scroll')
            warn('Setting vscrollbar-policy to AUTOMATIC')

        if hscroll_mode == "":
            self.set_property('hscrollbar-policy', Gtk.PolicyType.AUTOMATIC)
            warn(f'Invalid scroll mode "{hscroll}" for vertical scroll')
            warn('Setting hscrollbar-policy to AUTOMATIC')




class ScrollableBox(Scrollable, Box, ShellWidget):
    def __init__(self, spacing=0, vertical=False, children=[], homogeneous=False, **kwargs):
        Scrollable.__init__(self)
        Box.__init__(self, spacing=spacing, vertical=vertical, children=children, homogeneous=homogeneous)
        ShellWidget.__init__(self)