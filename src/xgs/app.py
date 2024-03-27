from xgs.style import info, warn, error
from xgs.widgets.window import Window
from xgs.utils import load_conf_file

from gi.repository import Gtk, Gio, GLib, Gdk

class _application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.github.XtremeTHN.XtremeGtkShell", 
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.file = ""

    def do_activate(self):
        Window.app = self
        
        info("Loading config file...")
        load_conf_file(self.file)
    
    def loadCss(self, css_file_path):
        def handle_parse_error(css_prov, css_section: Gtk.CssSection, error: GLib.Error):
            warn(f"CSS Error: {error.message} in file {css_section.get_file().get_path()}, at line {css_section.get_start_location().lines}")
            
        # css_file = Gio.File.new_for_path(css_file_path)
        if GLib.file_test(css_file_path, GLib.FileTest.EXISTS) is False:
            warn(f"'{css_file_path}' CSS File doesn't exists")
            return
        
        css = Gtk.CssProvider.new()
        css.connect('parsing-error', handle_parse_error)
        
        css.load_from_path(css_file_path)
        
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        
Application = _application()