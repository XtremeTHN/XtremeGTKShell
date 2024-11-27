from gi.repository import Gtk

from xgs.style import error, warn

from typing import Callable

class Bindable:
    def __init__(self, widget, prop):
        self.is_bindable = True
        
        self.bindable_widget: Gtk.Widget = widget
        self.bindable_prop_name: str = prop
        self.bindable_transform_func = None
            
    def transform(self, function: Callable):
        # def wrapper()
        if callable(function) is True:
            self.bindable_transform_func = function
        return self