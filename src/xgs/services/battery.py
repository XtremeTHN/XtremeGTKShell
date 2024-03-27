from gi.repository import GObject, GLib, Gio
# from xgs.utils import setInterval

class DeviceState:
    CHARGING = 1
    FULLY_CHARGED = 4

class Battery(GObject.GObject):
    percentage = GObject.Property(type=int, minimum=0, maximum=100, default=0, nick="percentage")
    charging = GObject.Property(type=bool, default=False, nick="charging")
    available = GObject.Property(type=bool, default=False, nick="available")
    charged = GObject.Property(type=bool, default=False, nick="charged")
    icon_name = GObject.Property(type=str, default="battery-caution-symbolic", nick="icon-name")
    time_remaining = GObject.Property(type=int, default=0, nick="time-remaining")
    energy = GObject.Property(type=int, default=0, nick="energy")
    energy_full = GObject.Property(type=int, default=0, nick="energy-full")
    energy_rate = GObject.Property(type=int, default=0, nick="energy-rate")
    def __init__(self):
        super().__init__()

        self.proxy = Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SYSTEM, Gio.DBusProxyFlags.NONE, 
                                       None, "org.freedesktop.UPower", 
                                       "/org/freedesktop/UPower/devices/DisplayDevice", "org.freedesktop.DBus.Properties",
                                       None)
        
        self.proxy.connect('g-signal', self._on_properties_changed)
        
        # GLib.idle_add(self.sync)
        self.sync() 
        self.__props: dict = None
    
    def _on_properties_changed(self, proxy, sender_name, signal_name, params: GLib.Variant):
        if signal_name == "PropertiesChanged":
            self.sync()
        else:
            service_debug(f"Unknown signal recieved '{signal_name}'")
        
    def sync(self, *args):
        self.proxy.GetAll("(s)", "org.freedesktop.UPower.Device", result_handler=self.__update_all_props)


    # def sync(self):
    #     self.get_props()
        # return GLib.SOURCE_CONTINUE
        
    def __update_all_props(self, _, result, __):
        if isinstance(result, Exception):
            print(result)
            return
        
        self.__props = result
        
        if self.get_prop_from_proxy(None, "IsPresent") is False:
            self.available = False
            return
                
        self.percentage = self.get_prop_from_proxy("percentage", "Percentage")
        self.charging = self.get_prop_from_proxy("charging", "State") == DeviceState.CHARGING
        self.charged = self.get_prop_from_proxy("charged","State") == DeviceState.FULLY_CHARGED or \
            self.get_prop_from_proxy("charged", "State") == DeviceState.CHARGING and \
            self.percentage == 100
        
        self.battery_icon_level = round(self.percentage / 10) * 10

        self.battery_icon_state = "-charging" if self.get_prop_from_proxy(None, "State") == DeviceState.CHARGING else ""

        self.icon_name = "battery-level-100-charged-symbolic" if self.charged else f"battery-level-{self.battery_icon_level}{self.battery_icon_state}-symbolic"
        self.notify("icon-name")

        self.time_remaining = self.get_prop_from_proxy("time-remaining", "TimeToFull") if self.charging else self.get_prop_from_proxy("time_remaining", "TimeToEmpty")

        self.energy = self.get_prop_from_proxy("energy", "Energy")
        self.energy_full = self.get_prop_from_proxy("energy-full", "EnergyFull")
        self.energy_rate = self.get_prop_from_proxy("energy-rate", "EnergyRate")

    def get_prop_from_proxy(self, self_prop, upower_prop):
        if self_prop is not None:
            self.notify(self_prop)
        return self.__props[upower_prop]


# class Battery:
#     def __init__(self) -> None:
#         self.con = Gio.DBusObjectManagerClient(
#             bus_type=Gio.BusType.SYSTEM,
#             flags=Gio.DBusObjectManagerClientFlags.NONE,
#             object_path="/org/freedesktop/UPower/devices/DisplayDevice"
#         )
        
#         self.con.connect("interface-proxy-properties-changed", self.__on_props_changed)
    
#     def __on_props_changed(self,
#                            dbus_client: Gio.DBusObjectManagerClient,
#                            object_proxy: Gio.DBusObjectProxy,
#                            interface_proxy: Gio.DBusProxy,
#                            changed_props: GLib.Variant,
#                            invalidated_props: list):
        
#         print(changed_props.unpack())
        
def commands(batt):
    exec_locals = {"batt":batt}
    while True:
        try:
            cmd = input("> ")
            if cmd in exec_locals:
                print(cmd)
                continue
            exec(cmd, {}, exec_locals)
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(e, " ".join(e.args))
            continue

bat = Battery()

import threading
threading.Thread(target=commands, args=[bat]).start()

GLib.MainLoop().run()