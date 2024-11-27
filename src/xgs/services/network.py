import gi
import threading

gi.require_version("NM", "1.0")

from gi.repository import NM, GObject, GLib
from typing import Callable, LiteralString

from xgs.services.service import Service
from xgs.style import warn, debug

_ACCESS_POINT_ICON = [
    [80, 'network-wireless-signal-excellent-symbolic'],
    [60,  'network-wireless-signal-good-symbolic'],
    [40, 'network-wireless-signal-ok-symbolic'],
    [20, 'network-wireless-signal-weak-symbolic'],
    [0, 'network-wireless-signal-none-symbolic'],
];

def _get_network_device(_type: NM.DeviceType, client: NM.Client):
    devices = list(filter(lambda x: x.get_device_type() == _type, client.get_devices()))
    return devices[-1] if len(devices) > 0 else None

def _connect_multiple(_object: GObject.GObject, *signals_and_handler: tuple[LiteralString, Callable]):
    for sh in signals_and_handler:
        connect_id = _object.connect(sh[0], sh[1])
        if hasattr(_object, "__signals_ids") is True:
            _object.__signals_ids.append(connect_id)
            
class AccessPoint(Service):
    def __init__(self, access_point: NM.AccessPoint, active: bool):
        super().__init__()
        
        if access_point.props.ssid is not None:
            self.ssid: str = access_point.props.ssid.get_data().decode()
        else:
            self.ssid: str = ""
            
        self.last_seen: int = access_point.props.last_seen
        self.strength: int = access_point.props.strength
        self.icon_name: str = list(filter(lambda threshold: threshold[0] <= self.strength, _ACCESS_POINT_ICON))[0][1]
        self.active: bool = active
    
class Wifi(Service):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ())
    }
    def __init__(self, client: NM.Client) -> None:
        super().__init__()
        
        self.__signals_ids: list[int] = []
        
        self.__client = client
        self.device: NM.DeviceWifi = _get_network_device(NM.DeviceType.WIFI, client)
        
        self.__aps: list[AccessPoint] = []
        
        self.__client.connect("notify::wireless-enabled", self.__activate)
        
        if self.__client.props.wireless_enabled:
            self.__activate()
    
    def __activate(self, *_):
        if self.__client.props.wireless_enabled is True:
            self.enabled = True
            
            self.device.request_scan_async()
            _connect_multiple(self.device,
                            ["notify::access-points", lambda *_: threading.Thread(target=self.__update_ap).start()],
                            ["access-point-added", lambda *_: self.emit("changed")],
                            ["access-point-removed", lambda *_: self.emit("changed")])
        else:
            self.enabled = False
            for x in self.__signals_ids:
                try:
                    self.__client.disconnect(x)
                except:
                    warn(f"Couldn't disconnect signal id {x}")
            
    def __update_ap(self):
        active_ap = self.device.get_active_access_point()
        try:
            self.__aps = [AccessPoint(x, x.props.ssid == active_ap.props.ssid) for x in self.device.get_access_points()]
        except Exception as e:
            warn("Exception ocurred when trying to convert access_points from NetworkManager to AccessPoints class")
            warn(f"{e.__class__.__name__}: ", " ".join(e.args))
        
    @GObject.Property(nick="enabled")
    def enabled(self):
        return self.__client.wireless_get_enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.notify("enabled")
        self.__client.wireless_set_enabled(enabled)
        
    @GObject.Property(nick="access-points")
    def access_points(self):
        self.notify("access-points")
        return self.__aps
        
    def scan(self, cb=None):
        """Starts an async scan

        Args:
            cb (callable, optional): A callback, it will be called when scan finishes. Needs to accept this three arguments, src_obj: Network, res, user_data. Defaults to None.
        """
        self.device.request_scan_async(callback=cb)

Network = Wifi(NM.Client.new())
# TestService(network=Network)

GLib.MainLoop().run()