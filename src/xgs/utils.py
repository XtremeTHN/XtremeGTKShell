import importlib.util
import threading
import time
import sys
import os

from gi.repository import GObject, Gio, Gtk, GLib

from xgs.style import info, warn, debug, error

CONFIG_PATH=os.path.expanduser("~/.config/xgs")

class GArray(GObject.GObject):
    def __init__(self):
        super().__init__()

        self.list = []

    def append(self, obj: object):
        self.list.append(obj)

    def remove(self, obj: object):
        self.list.remove(obj)

    def find(self, obj):
        try:
            return self.list.index(obj)
        except ValueError:
            return -1

class setInterval :
    def __init__(self,interval, callback) :
        self.interval=interval
        self.action=callback
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action(self)

    def cancel(self) :
        self.stopEvent.set()

class setTimeout:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.cb = callback
        threading.Thread(target=self.__timeout()).start()

    def __timeout(self):
        time.sleep(self.timeout)
        self.cb()

def include_file(file_path, bytes=False):
    file = Gio.File.new_for_path(file_path)
    if file.query_exists() is False:
        msg = f"File '{file_path}' doesn't exists"
        error(msg)
        raise FileNotFoundError(msg)
    
    # Return string if bytes is True, else return bytes
    return file.load_contents()[2 if bytes is False else 1]

def lookupIcon(icon, size=16):
    if icon is None:
        return
    
    return Gtk.IconTheme.new().lookup_icon(icon, None, size, 0, Gtk.TextDirection.NONE, Gtk.IconLookupFlags.PRELOAD)

def iconExists(icon_name):
    return Gtk.IconTheme.new().has_icon(icon_name)

def load_conf_file(path):
    path = os.path.expanduser(path)
    
    if os.path.exists(path):
        debug(f"Loading config script from '{path}'...")
        
        spec = importlib.util.spec_from_file_location("Config", path)
        if spec is None:
            error("Failed to load config script. spec is None")
            sys.exit(1)
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        error(f"Config file '{path}' doesn't exists")
        
def TestService(**_locals):
    def commands(_locals: dict):
        exec_locals = _locals
        while True:
            try:
                cmd = input("> ")
                
                print(exec_locals.get(cmd))
                exec(cmd, {}, exec_locals)
            except (KeyboardInterrupt, EOFError):
                break
            except Exception as e:
                print(e, " ".join(e.args))
                continue

    threading.Thread(target=commands, args=[_locals]).start()

    GLib.MainLoop().run()