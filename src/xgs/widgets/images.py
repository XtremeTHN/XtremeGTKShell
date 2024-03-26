from xgs.widgets.misc import ShellWidget, Bindable
from xgs.style import info, warn, error
from xgs.utils import iconExists
from gi.repository import Gtk, Gio

from typing import Literal

class Icon(Gtk.Image, ShellWidget):
    def __init__(self, icon: Bindable | str, size=16):
        if iconExists(icon) is False:
            warn(f"Icon '{icon}' doesn't exists")
        
        Gtk.Image.__init__(self, pixel_size=size)
        if isinstance(icon, Bindable) is True:
            self.bind_property("icon-name", icon, icon.bindable_prop_name, transform_to=icon.bindable_transform_func)
        else:
            self.set_from_icon_name(icon)
            
        ShellWidget.__init__(self)
        
class Image(Gtk.Picture, ShellWidget):
    def __init__(self, image_path="", content_fit: Literal["fill", "contain", "cover", "scale_down"]="", keep_aspect_ratio=False, can_shrink=True):
        file = Gio.File.new_for_path(image_path)
        if file.query_exists() is False:
            warn(f"File {image_path} doesn't exists")
        
        Gtk.Picture.__init__(file=file, content_fit=getattr(Gtk.ContentFit, content_fit, Gtk.ContentFit.FILL), 
                             keep_aspect_ratio=keep_aspect_ratio, can_shrink=can_shrink)
        
        ShellWidget.__init__(self)