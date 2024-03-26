from gi.repository import GObject, GLib, Gio

class DeviceState:
    CHARGING = 1
    FULLY_CHARGED = 4

class Battery(GObject.GObject):
    def __init__(self):
        super().__init__()

        self.proxy = Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION, Gio.DBusProxyFlags.NONE, 
                                       None, "org.freedesktop.UPower", 
                                       "/org/freedesktop/UPower", "org.freedesktop.UPower.Device", 
                                       None)
        
        self.proxy.connect("g-properties-changed", self._on_properties_changed)

        self.percentage = GObject.Property(type=int, minimum=0, maximum=100, default_value=0)
        self.charging = GObject.Property(type=bool, default_value=False)
        self.available = GObject.Property(type=bool, default_value=False)
        self.charged = GObject.Property(type=bool, default_value=False)
        self.icon_name = GObject.Property(type=str, default_value="battery-caution-symbolic")
        self.time_remaining = GObject.Property(type=int, default_value=0)
        self.energy = GObject.Property(type=int, default_value=0)
        self.energy_full = GObject.Property(type=int, default_value=0)
        self.energy_rate = GObject.Property(type=int, default_value=0)
    
    def _on_properties_changed(self, *args):
        self.__sync()

    def __sync(self):
        if self.proxy.get_property("IsPresent") is False:
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

        self.time_remaining = self.get_prop_from_proxy("time_remaining", "TimeToFull") if self.charging else self.get_prop_from_proxy("time_remaining", "TimeToEmpty")

        self.energy = self.get_prop_from_proxy("energy", "Energy")
        self.energy_full = self.get_prop_from_proxy("energy_full", "EnergyFull")
        self.energy_rate = self.get_prop_from_proxy("energy_rate", "EnergyRate")

    def get_prop_from_proxy(self, self_prop, upower_prop):
        if self_prop is not None:
            self.notify(self_prop)
        return self.proxy.get_property(upower_prop)