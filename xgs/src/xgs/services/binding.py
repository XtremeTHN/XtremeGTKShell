from gi.repository import Gtk

from xgs.style import error, warn

from typing import Callable

class Bindable(Gtk.Widget):
    def __init__(self):
        self.bindable_widget = self
        self.bindable_prop_name = ""
        self.bindable_transform_func = None

    def bind(self,prop: str):
        prop_spec = self.bindable_widget.find_property(prop)
        self.bindable_prop_name = ""
        if prop_spec is not None:
            self.bindable_prop_name = prop
            return self
        else:
            error("No such property")
            raise ValueError(f"The property {prop} doesn't exists")
    
    def transform(self, function: Callable):
        if callable(function) is True:
            self.bindable_transform_func = function
            