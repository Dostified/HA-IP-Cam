from homeassistant.components.select import SelectEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ms_ip_cam"

class MSCamSelectEntity(SelectEntity):
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

class MSCamLensSelect(MSCamSelectEntity):
    """Lens selection entity for MS IP Cam."""
    
    def __init__(self, entry_id, ip_address: str, http_port: int):
        super().__init__(entry_id, ip_address, http_port)
        self._attr_name = "Lens Switcher"
        self._attr_unique_id = f"{entry_id}_lens"
        self._attr_icon = "mdi:camera-flip"
        self._attr_options = ["Main", "Front", "Ultrawide", "Telephoto"]
        self._attr_current_option = "Main"
        self._map = {"Main": "main", "Front": "front", "Ultrawide": "ultrawide", "Telephoto": "telephoto"}
        self._reverse_map = {v: k for k, v in self._map.items()}

    async def async_update(self):
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(f"http://{self._ip}:{self._port}/status", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    lens = data.get("lens", "main")
                    self._attr_current_option = self._reverse_map.get(lens, "Main")
                    self._attr_available = True
                else:
                    self._attr_available = False
        except Exception:
            self._attr_available = False

    async def async_select_option(self, option: str) -> None:
        lens_param = self._map.get(option, "main")
        try:
            session = async_get_clientsession(self.hass)
            await session.get(f"http://{self._ip}:{self._port}/lens?type={lens_param}", timeout=3)
            self._attr_current_option = option
        except Exception:
            pass


class MSCamModeSelect(MSCamSelectEntity):
    def __init__(self, entry_id, ip_address: str, http_port: int):
        super().__init__(entry_id, ip_address, http_port)
        self._attr_name = "Operating Mode"
        self._attr_unique_id = f"{entry_id}_mode"
        self._attr_icon = "mdi:cog"
        self._attr_options = ["On-Demand", "Always On (24/7)"]
        self._attr_current_option = "On-Demand"

    async def async_update(self):
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(f"http://{self._ip}:{self._port}/status", timeout=2) as response:
                if response.status == 200:
                    data = await response.json()
                    mode = data.get("mode", "on_demand")
                    self._attr_current_option = "Always On (24/7)" if mode == "always_on" else "On-Demand"
        except Exception:
            pass

    async def async_select_option(self, option: str) -> None:
        mode_param = "always_on" if option == "Always On (24/7)" else "on_demand"
        try:
            session = async_get_clientsession(self.hass)
            await session.get(f"http://{self._ip}:{self._port}/mode?type={mode_param}", timeout=3)
            self._attr_current_option = option
        except Exception:
            pass


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MSCamLensSelect(entry.entry_id, data["ip_address"], data["http_port"]),
        MSCamModeSelect(entry.entry_id, data["ip_address"], data["http_port"])
    ])
