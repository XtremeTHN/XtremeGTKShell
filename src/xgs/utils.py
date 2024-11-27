import importlib.util
import threading
import shlex
import time
import sys
import os

from gi.repository import GObject, Gio, Gtk, GLib

from xgs.style import info, warn, debug, error
from typing import Callable

from subprocess import Popen, PIPE

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
    def __init__(self,interval, callback):
        """Execute a function every x milliseconds

        Args:
            interval (int): The interval in milliseconds
            callback (function): The callback that will be executed
        """
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
        """Runs a function after an specified time

        Args:
            timeout (int): Timeout in miliseconds
            callback (function): The callback
        """
        self.timeout = timeout
        self.cb = callback
        threading.Thread(target=self.__timeout()).start()

    def __timeout(self):
        time.sleep(self.timeout)
        self.cb()

def include_file(file_path, bytes=False):
    """Loads a file with Gio.File

    Args:
        file_path (str): The file path
        bytes (bool, optional): If it should return bytes. Defaults to False.

    Raises:
        FileNotFoundError: If the file is not found

    Returns:
        str | bytes: The file content
    """
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
    """Checks if an icon exists.

    Args:
        icon_name (str): The icon name you want to know if it exists

    Returns:
        bool
    """
    return Gtk.IconTheme.new().has_icon(icon_name)

def load_conf_file(path):
    """Loads a config file.

    Args:
        path (str): The config file path
    """
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
        
def execute(cmd: str):
    """Executes a shell command with subprocess module. The command will be splited with shlex

    Args:
        cmd (str): The cmd
    """
    if cmd is not None:
        with Popen(args=shlex.split(cmd), stdout=PIPE, text=True) as proc:
            stdout, _ = proc.communicate()
            return stdout
    else:
        warn("cmd is None")

def executeAsync(cmd: str):
    proc = Popen(args=shlex.split(cmd if cmd is not None else ""))
    return proc

def spawn_threaded(func: Callable, *args):
    """Executes a function on another thread

    Args:
        func (Callable): The function that will be called

    Returns:
        threading.Thread: The thread object
    """
    thread = threading.Thread(target=func, args=args)
    return thread

def TestService(**_locals):
    """Runs a python shell for executing python cmds. Made for debugging services.
    """
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

    info("GLib Mainloop started...")
    GLib.MainLoop().run()