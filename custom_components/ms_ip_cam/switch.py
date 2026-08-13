from homeassistant.components.switch import SwitchEntity
import requests

ANDROID_IP = "192.168.1.100"

class FlashlightSwitch(SwitchEntity):
    def __init__(self):
        self._attr_name = "Android Camera Flashlight"
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        try:
            requests.get(f"http://{ANDROID_IP}:8080/flash?state=on", timeout=3)
            self._is_on = True
        except requests.exceptions.RequestException:
            pass

    def turn_off(self, **kwargs):
        try:
            requests.get(f"http://{ANDROID_IP}:8080/flash?state=off", timeout=3)
            self._is_on = False
        except requests.exceptions.RequestException:
            pass

# Remove setup_platform and replace it with this:
async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the switch from a config entry."""
    ip_address = entry.data["ip_address"]
    async_add_entities([FlashlightSwitch(ip_address)])
