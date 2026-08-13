from homeassistant.components.select import SelectEntity
import requests

class MSCamLensSelect(SelectEntity):
    """Lens Switcher Entity."""
    def __init__(self, ip_address: str, http_port: int):
        self._attr_name = "MS IP Cam Lens Switcher"
        self._attr_icon = "mdi:camera-flip"
        self._attr_options = ["Main (Back)", "Ultrawide", "Telephoto", "Front (Selfie)"]
        self._attr_current_option = "Main (Back)"
        self._ip = ip_address
        self._port = http_port

    def select_option(self, option: str) -> None:
        lens_map = {
            "Main (Back)": "main",
            "Ultrawide": "ultrawide",
            "Telephoto": "telephoto",
            "Front (Selfie)": "front"
        }
        lens_param = lens_map.get(option, "main")
        try:
            requests.get(f"http://{self._ip}:{self._port}/lens?type={lens_param}", timeout=3)
            self._attr_current_option = option
        except requests.exceptions.RequestException:
            pass

class MSCamModeSelect(SelectEntity):
    """Operating Mode Entity."""
    def __init__(self, ip_address: str, http_port: int):
        self._attr_name = "MS IP Cam Operating Mode"
        self._attr_icon = "mdi:cog"
        self._attr_options = ["On-Demand", "Always On (24/7)"]
        self._attr_current_option = "On-Demand"
        self._ip = ip_address
        self._port = http_port

    def select_option(self, option: str) -> None:
        mode_param = "always_on" if option == "Always On (24/7)" else "on_demand"
        try:
            requests.get(f"http://{self._ip}:{self._port}/mode?type={mode_param}", timeout=3)
            self._attr_current_option = option
        except requests.exceptions.RequestException:
            pass

async def async_setup_entry(hass, entry, async_add_entities):
    ip_address = entry.data["ip_address"]
    http_port = entry.data.get("http_port", 8080)
    async_add_entities([
        MSCamLensSelect(ip_address, http_port),
        MSCamModeSelect(ip_address, http_port)
    ])
