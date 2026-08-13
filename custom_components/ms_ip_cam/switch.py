from homeassistant.components.switch import SwitchEntity
import requests

DOMAIN = "ms_ip_cam"

class FlashlightSwitch(SwitchEntity):
    def __init__(self, ip_address: str, http_port: int):
        self._attr_name = "MS IP Cam Flashlight"
        self._is_on = False
        self._ip = ip_address
        self._port = http_port

    @property
    def is_on(self):
        return self._is_on

    def update(self):
        """Poll the camera app for status to keep two-way sync in check."""
        try:
            res = requests.get(f"http://{self._ip}:{self._port}/status", timeout=2)
            if res.status_code == 200:
                self._is_on = res.json().get("flash", False)
        except requests.exceptions.RequestException:
            pass

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
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([FlashlightSwitch(data["ip_address"], data["http_port"])])
