from xgs.widgets.window import Window
from xgs.widgets.box import Box
from xgs.widgets.centerbox import CenterBox
from xgs.widgets.label import Label

import gi
gi.require_version("Adw","1")
from gi.repository import Gtk, Adw

Adw.init()

def TopBarContent():
    return CenterBox(
        vertical=False,
        startWidget=Box(
            spacing=20,
            vertical=False,
            children=[
                Label(label="17/1/2024"),
                Label(label="3:49")
            ],
            hexpand=True,
            vexpand=False,
        ),
        centerWidget=Label(label="Panda eyes - Galaxica",
                           hexpand=True),
        endWidget=Label(label="Ok", hexpand=True)
    )

def TopBarWindow(): 
    return Window(
        "test",
        child=TopBarContent(),
        layer="top",
        anchor=["top","left","right"],
        exclusive=False
    )

TopBarWindow()
