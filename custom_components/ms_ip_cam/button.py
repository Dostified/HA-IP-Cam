from homeassistant.components.button import ButtonEntity
import requests

DOMAIN = "ms_ip_cam"

class CameraShutterButton(ButtonEntity):
    def __init__(self, ip_address: str, http_port: int):
        self._attr_name = "MS IP Cam Shutter Button"
        self._attr_icon = "mdi:camera-iris"
        self._ip = ip_address
        self._port = http_port

    def press(self) -> None:
        try:
            requests.get(f"http://{self._ip}:{self._port}/shutter", timeout=3)
        except requests.exceptions.RequestException:
            pass

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CameraShutterButton(data["ip_address"], data["http_port"])])
