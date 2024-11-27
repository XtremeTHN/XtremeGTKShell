from xgs.widgets.misc import ShellWidget, Bindable
from xgs.style import info, warn, error
from xgs.utils import iconExists
from gi.repository import Gtk, Gio, GLib

from typing import Literal

class Icon(Gtk.Image, ShellWidget):
    def __init__(self, icon: Bindable | str, size=16, **kwargs):
        # if iconExists(icon) is False:
        #     warn(f"Icon '{icon}' doesn't exists")
        
        Gtk.Image.__init__(self, pixel_size=size, **kwargs)
        if isinstance(icon, Bindable) is True:
            self._create_binding(icon)
        else:
            self.set_from_icon_name(icon)
            
        ShellWidget.__init__(self)
        
class Image(Gtk.Picture, ShellWidget):
    def __init__(self, image_path: Bindable | str="", content_fit: Literal["fill", "contain", "cover", "scale_down"]="", keep_aspect_ratio=False, can_shrink=True, **kwargs):
        Gtk.Picture.__init__(content_fit=getattr(Gtk.ContentFit, content_fit, Gtk.ContentFit.FILL), 
                        keep_aspect_ratio=keep_aspect_ratio, can_shrink=can_shrink, **kwargs)
        
        if isinstance(image_path, Bindable):
            self._create_binding(image_path, self.set_filename, str)
        else:
            if GLib.file_test(image_path, GLib.FileTest.EXISTS) is False:
                warn(f"File {image_path} doesn't exists")
    
        ShellWidget.__init__(self)