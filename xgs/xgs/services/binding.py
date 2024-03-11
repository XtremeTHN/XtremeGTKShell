from gi.repository import Gtk

class Binded:
    def __init__(self)

class Bindable:
    def __init__(self, widget: Gtk.Widget):
        self.widget = widget

    def bind(self,prop, transform_func=None):
        prop_spec = self.widget.find_property(prop)
        self.prop_name = ""
        if prop_spec is not None:
            self.prop_name = prop
        else:
            raise ValueError(f"The property {prop} doesn't exists")

    
