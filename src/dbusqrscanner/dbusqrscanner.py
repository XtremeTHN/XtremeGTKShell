"""Main module."""
#!/usr/bin/env python3
import dbus

from dbus.service import Object, BusName, method, signal
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib
from .scanner import Scanner

DBusGMainLoop(set_as_default=True)

class QRService(Object):
    def __init__(self, msgs=False):
        self.mainloop = GLib.MainLoop()
        self.show_messages = msgs

        self.log("Creating DBus service...")
        self.bus = dbus.SessionBus()
        self.name = BusName("com.github.XtremeTHN.QRScanner", self.bus)

        super().__init__(self.bus, "/com/github/XtremeTHN/QRScanner", self.name)
        self.log("Done")

        self.scanner = Scanner(self)

    def run(self):
        try:
            self.mainloop.run()
        except:
            pass

    def log(self, msg, log_level="INFO"):
        if self.show_messages is True:
            print(log_level + ":", msg)

    @method(dbus_interface="com.github.XtremeTHN.QRScanner")
    def StartScan(self):
        self.scanner.scan()

    @signal(dbus_interface="com.github.XtremeTHN.QRScanner", signature="s")
    def DetectedQR(self, content: str):
        pass
