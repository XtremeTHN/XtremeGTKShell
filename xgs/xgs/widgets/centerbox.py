from xgs.widgets.misc import ShellWidget

from gi.repository import Gtk

class CenterBox(Gtk.CenterBox, ShellWidget):
    def __init__(self, vertical=False, startWidget=None, centerWidget=None, endWidget=None, **kwargs):
        Gtk.CenterBox.__init__(self,
                               orientation=Gtk.Orientation.VERTICAL if not vertical else Gtk.Orientation.HORIZONTAL,
                               **kwargs)
        
        ShellWidget.__init__(self)

        if startWidget is not None:
            self.set_start_widget(startWidget)
        elif centerWidget is not None:
            self.set_center_widget(centerWidget)
        else:
            self.set_end_widget(endWidget)
            