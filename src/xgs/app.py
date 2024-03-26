from xgs.style import info, warn, error
from xgs.widgets.window import Window
from xgs.utils import load_conf_file

from gi.repository import Gtk, Gio

class _application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.github.XtremeTHN.XtremeGtkShell", 
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.file = ""

    def do_activate(self):
        Window.app = self
        
        info("Loading config file...")
        load_conf_file(self.file)
        
Application = _application()