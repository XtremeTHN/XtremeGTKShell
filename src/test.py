from xgs.widgets.window import Window
from xgs.widgets.scroll import Scrollable
from xgs.widgets.label import Label

import gi
gi.require_version("Adw","1")
from gi.repository import Gtk, Adw

Adw.init()

def TopBarWindow(): 
    # return Window(
    #     "test", 
    #     child=Box(
    #         vertical=False, 
    #         spacing=5,
    #         children=[
    #             Gtk.Label(label="kitty")
    #         ]),
    #     anchor=['top','left','right']
    # )
    return Window(
        "test",
        child=Label(label="Hi"),
        layer="top",
        anchor=["top","left","right"],
        exclusive=False
    )

TopBarWindow()
