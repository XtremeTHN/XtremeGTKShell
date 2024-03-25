from ctypes import CDLL
import importlib.util

CDLL('libgtk4-layer-shell.so')

import os
import gi
gi.require_versions({'Gtk': '4.0', 'Gtk4LayerShell': '1.0'})

from gi.repository import Gtk

from xgs.widgets.window import Window
from xgs.style import warn, debug, error, info

import argparse
import sys

CONFIG_PATH=os.path.expanduser("~/.config/xgs")

def load_conf_file(path=None):
    if path is None:
        path = CONFIG_PATH
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, 'config.py')
    
    if os.path.exists(path):
        debug(f"Loading config script from '{path}'...")
        
        spec = importlib.util.spec_from_file_location("Config", path)
        if spec is None:
            error("Failed to load config script. spec is None")
            sys.exit(1)
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        print("Asd")
        error("Config file doesn't exists")

def main():
    def on_activate(app, file):
        Window.app = app
        
        info("Loading config file...")
        load_conf_file(file)
    
    parser = argparse.ArgumentParser(prog="xgs", description="XtremeGtkShell is heavily inspired of Aylur's Gtk Shell")
    
    parser.add_argument("-c", "--config", action="store", help="A path pointing to a config file")
    parser.add_argument("-d", "--debug", action="store", help="If it's true, then it will show debug messages")
    
    args = parser.parse_args()
    
    app = Gtk.Application(application_id='com.github.XtremeTHN.XtremeGtkShell')
    app.connect('activate', on_activate, args.config)
    try:
        app.run([])
    except (KeyboardInterrupt, EOFError):
        warn("Exiting...")

if __name__ == "__main__":
    main()