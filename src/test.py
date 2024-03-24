from xgs.widgets.window import Window
from xgs.widgets.scroll import Scrollable
from xgs.widgets.box import Box

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
        child=Scrollable(
            vscroll="always",
            hscroll="always",
            child=Box(
                children=[
                    Gtk.Label(label="kitty")
                ]
            )
        )
    )

TopBarWindow()
