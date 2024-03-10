from ctypes import CDLL
import importlib.util

#CDLL('/usr/local/lib/libgtk4-layer-shell.so')
CDLL('libgtk4-layer-shell.so')

import os
import gi
gi.require_versions({'Gtk': '4.0', 'Gtk4LayerShell': '1.0'})

from gi.repository import Gtk
from gi.repository import Gtk4LayerShell

CONFIG_PATH=os.path.expanduser("~/.config/xgs")

def load_conf_file(path=None):
    if path is None:
        path = CONFIG_PATH
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, 'config.py')
    
    if os.path.exists(path):
        spec = importlib.util.spec_from_file_location("Config", path)
        if spec is None:
            print("failed. see source code for more information")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        print(dir(module))
    else:
        print("config file doesn't exists")

def init():
    def on_activate(app):
        load_conf_file("./src/test.py")

    app = Gtk.Application(application_id='com.github.XtremeTHN.XtremeGtkShell')
    app.connect('activate', on_activate)

    app.run([])

if __name__ == "__main__":
    init()
