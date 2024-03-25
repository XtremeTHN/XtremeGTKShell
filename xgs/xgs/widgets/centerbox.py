from xgs.widgets.misc import ShellWidget

from gi.repository import Gtk

class CenterBox(Gtk.CenterBox, ShellWidget):
    def __init__(self, vertical=False, startWidget=None, centerWidget=None, endWidget=None, **kwargs):
        Gtk.CenterBox.__init__(self, start_widget=startWidget, center_widget=centerWidget, end_widget=endWidget,
                               orientation=Gtk.Orientation.VERTICAL if vertical is True else Gtk.Orientation.HORIZONTAL,
                               **kwargs)
        
        ShellWidget.__init__(self)