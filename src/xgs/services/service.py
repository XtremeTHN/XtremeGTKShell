from xgs.services.binding import Bindable
from xgs.style import error

from gi.repository import GObject

class Service(GObject.GObject):
    def __init__(self):
        super().__init__()
        
    def bind(self, prop):
        prop_spec = self.find_property(prop)
        if prop_spec is not None:
            return Bindable(self, prop)
        else:
            error("No such property")
            raise ValueError(f"The property {prop} doesn't exists")