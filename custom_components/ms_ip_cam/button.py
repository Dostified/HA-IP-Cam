from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = "ha_ip_camera"

class CameraShutterButton(ButtonEntity):
    _attr_has_entity_name = True
    
    def __init__(self, entry_id, ip_address: str, http_port: int):
        self._entry_id = entry_id
        self._attr_name = "Shutter Button"
        self._attr_unique_id = f"{entry_id}_shutter"
        self._attr_icon = "mdi:camera-iris"
        self._ip = ip_address
        self._port = http_port

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            session = async_get_clientsession(self.hass)
            await session.get(f"http://{self._ip}:{self._port}/shutter", timeout=3)
        except Exception:
            pass

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CameraShutterButton(entry.entry_id, data["ip_address"], data["http_port"])])
