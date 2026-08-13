from homeassistant.components.switch import SwitchEntity
import requests

class FlashlightSwitch(SwitchEntity):
    def __init__(self, ip_address: str):
        self._attr_name = "MS IP Cam Flashlight"
        self._is_on = False
        self._ip = ip_address # Saves the dynamic IP

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        try:
            requests.get(f"http://{self._ip}:8080/flash?state=on", timeout=3)
            self._is_on = True
        except requests.exceptions.RequestException:
            pass

    def turn_off(self, **kwargs):
        try:
            requests.get(f"http://{self._ip}:8080/flash?state=off", timeout=3)
            self._is_on = False
        except requests.exceptions.RequestException:
            pass

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the switch from a config entry."""
    ip_address = entry.data["ip_address"]
    async_add_entities([FlashlightSwitch(ip_address)])
