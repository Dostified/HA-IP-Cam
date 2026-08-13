from homeassistant.components.switch import SwitchEntity
import requests

class FlashlightSwitch(SwitchEntity):
    def __init__(self, ip_address: str, http_port: int):
        self._attr_name = "MS IP Cam Flashlight"
        self._is_on = False
        self._ip = ip_address
        self._port = http_port

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        try:
            requests.get(f"http://{self._ip}:{self._port}/flash?state=on", timeout=3)
            self._is_on = True
        except requests.exceptions.RequestException:
            pass

    def turn_off(self, **kwargs):
        try:
            requests.get(f"http://{self._ip}:{self._port}/flash?state=off", timeout=3)
            self._is_on = False
        except requests.exceptions.RequestException:
            pass

async def async_setup_entry(hass, entry, async_add_entities):
    ip_address = entry.data["ip_address"]
    http_port = entry.data.get("http_port", 8080)
    async_add_entities([FlashlightSwitch(ip_address, http_port)])
