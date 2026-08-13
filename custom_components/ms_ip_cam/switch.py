from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ha_ip_camera"

class HACamEntity(SwitchEntity):
    """Base entity for Home Assistant IP Camera."""
    _attr_has_entity_name = True
    
    def __init__(self, entry_id, ip_address, http_port):
        self._entry_id = entry_id
        self._ip = ip_address
        self._port = http_port

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
        }

class FlashlightSwitch(HACamEntity):
    """Flashlight control for Home Assistant IP Camera."""
    
    def __init__(self, entry_id, ip_address, http_port):
        super().__init__(entry_id, ip_address, http_port)
        self._attr_name = "Flashlight"
        self._attr_unique_id = f"{entry_id}_flashlight"
        self._attr_icon = "mdi:flashlight"
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_update(self):
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(f"http://{self._ip}:{self._port}/status", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    self._is_on = data.get("flash", False)
                    self._attr_available = True
                else:
                    self._attr_available = False
        except Exception:
            self._attr_available = False

    async def async_turn_on(self, **kwargs):
        try:
            session = async_get_clientsession(self.hass)
            await session.get(f"http://{self._ip}:{self._port}/flash?state=on", timeout=3)
            self._is_on = True
        except Exception:
            pass

    async def async_turn_off(self, **kwargs):
        try:
            session = async_get_clientsession(self.hass)
            await session.get(f"http://{self._ip}:{self._port}/flash?state=off", timeout=3)
            self._is_on = False
        except Exception:
            pass


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        FlashlightSwitch(entry.entry_id, data["ip_address"], data["http_port"])
    ])
