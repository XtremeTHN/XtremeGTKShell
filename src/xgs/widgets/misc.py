from gi.repository import Gtk
from gi.repository import Gtk4LayerShell as LayerShell
from typing import Callable, Any

from xgs.style import info, debug, error, warn
from xgs.services.binding import Bindable

class ShellWidget(Gtk.Widget):
    def __init__(self):
        ...
        
    def set_margins(self, margins: list[int], is_window=False):
        """
            Set's the margins.
            Reminder: margins = [top, right, bottom, left]
        """
        length = len(margins)
        
        top = margins[0]
        right = margins[1] if length > 1 else top
        bottom = margins[2] if length > 2 else right
        left = margins[3] if length > 3 else bottom
    
        debug(f"Setting margins: {top}, {right}, {bottom}, {left}")
        if is_window is True:
            LayerShell.set_margin(self, LayerShell.Edge.TOP, top)
            LayerShell.set_margin(self, LayerShell.Edge.RIGHT, right)
            LayerShell.set_margin(self, LayerShell.Edge.BOTTOM, bottom)
            LayerShell.set_margin(self, LayerShell.Edge.LEFT, left)
        else:
            self.set_margin_top(top)
            self.set_margin_end(right)
            self.set_margin_bottom(bottom)
            self.set_margin_start(left)

    def set_class_name(self, className: str):
        self.set_css_name(className)
    
    def toggle_class_name(self, className: str):
        if self.has_css_class(className):
            info("Removing css class: " + className + " to: " + self.get_name())
            self.remove_css_class(className)
        else:
            info("Adding css class: " + className + " to: " + self.get_name())
            self.add_css_class(className)
            
            
    def _create_binding(self, bind_obj: Bindable, setter_func: Callable, expected_type: object):
        def change(*_):
            value = bind_obj.bindable_widget.get_property(bind_obj.bindable_prop_name)
            if bind_obj.bindable_transform_func is not None:
                value = bind_obj.bindable_transform_func(value)
            
            if isinstance(value, str):
                setter_func(value)
            else:
                warn(f"Invalid type '{type(value).__name__}' expected {expected_type.__name__}")
                return
        bind_obj.bindable_widget.connect(f"notify::{bind_obj.bindable_prop_name}", change)
            
    def bind(self, prop):
        prop_spec = self.find_property(prop)
        if prop_spec is not None:
            return Bindable(self, prop)
        else:
            error("No such property")
            raise ValueError(f"The property {prop} doesn't exists")