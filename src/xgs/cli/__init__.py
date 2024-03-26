from ctypes import CDLL

CDLL('libgtk4-layer-shell.so')

import gi
gi.require_versions({'Gtk': '4.0', 'Gtk4LayerShell': '1.0'})

from xgs.style import warn, debug, error, info
from xgs.app import Application

import argparse

def main():

    parser = argparse.ArgumentParser(prog="xgs", description="XtremeGtkShell is heavily inspired of Aylur's Gtk Shell")
    
    parser.add_argument("-c", "--config", action="store", default="~/.config/xgs/config.py", help="A path pointing to a config file")
    parser.add_argument("-d", "--debug", action="store", help="If it's true, then it will show debug messages")
    parser.add_argument("-i", "--init", help="Initializes a virtual environment with pygobject and pygobject-stubs installed")
    
    args = parser.parse_args()    
    
    Application.file = args.config
    
    try:
        Application.run([])
    except (KeyboardInterrupt, EOFError):
        warn("Exiting...")

if __name__ == "__main__":
    main()
