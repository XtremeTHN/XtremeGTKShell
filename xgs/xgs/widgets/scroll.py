from xgs.services.binding import Bindable
from xgs.widgets.misc import ShellWidget
from xgs.style import warn, info
from gi.repository import Gtk

class Scrollable(Gtk.ScrolledWindow, ShellWidget):
    def __init__(self, vscroll="automatic", hscroll="automatic", child=None, **kwargs):
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




class ScrollableBox(Scrollable):
    def __init__(self, spacing=0, vertical=False, children=[], homogeneous=False, **kwargs):
        Scrollable.__init__(self)
        Bindable.__init__(self)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL if not vertical else Gtk.Orientation.VERTICAL,
                         spacing=spacing,
                         homogeneous=homogeneous,)
    