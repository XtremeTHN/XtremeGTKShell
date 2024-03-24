from gi.repository import Gtk

from xgs.style import error

class Bindable(Gtk.Widget):
    def __init__(self):
        self.bindable_widget = self
        self.bindable_prop_name = ""
        self.bindable_transform_func = None

    def bind(self,prop):
        prop_spec = self.bindable_widget.find_property(prop)
        self.bindable_prop_name = ""
        if prop_spec is not None:
            self.bindable_prop_name = prop
            return self
        else:
            error("Programming error")
            raise ValueError(f"The property {prop} doesn't exists")
    
    def transform(self, function):
        self.bindable_transform_func = function
