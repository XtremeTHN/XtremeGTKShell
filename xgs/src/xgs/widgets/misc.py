from gi.repository import Gtk
from xgs.style import info
from xgs.services.binding import Bindable

class ShellWidget(Bindable, Gtk.Widget):
    def __init__(self):
        Bindable.__init__(self)

    def set_margins(self, margins: list[int]):
        """
            Set's the margins.
            Reminder: margins = [top, right, bottom, left]
        """
        length = len(margins)
        
        top = margins[0]
        right = margins[1] if length > 1 else top
        bottom = margins[2] if length > 2 else right
        left = margins[3] if length > 3 else bottom
    
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