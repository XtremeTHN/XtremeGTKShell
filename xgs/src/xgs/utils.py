import time, threading

from gi.repository import GObject, Gio, GLib, Gtk, Gdk

from xgs.style import info, warn, error

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