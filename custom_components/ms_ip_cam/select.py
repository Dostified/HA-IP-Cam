from homeassistant.components.select import SelectEntity
import requests

DOMAIN = "ms_ip_cam"

class MSCamLensSelect(SelectEntity):
    def __init__(self, ip_address: str, http_port: int):
        self._attr_name = "MS IP Cam Lens Switcher"
        self._attr_icon = "mdi:camera-flip"
        self._attr_options = ["Main (Back)", "Ultrawide", "Telephoto", "Front (Selfie)"]
        self._attr_current_option = "Main (Back)"
        self._ip = ip_address
        self._port = http_port

    @property
    def current_option(self) -> str:
        return self._attr_current_option

    def update(self):
        """Sync live lens selection from the phone app."""
        try:
            res = requests.get(f"http://{self._ip}:{self._port}/status", timeout=2)
            if res.status_code == 200:
                lens = res.json().get("lens", "main")
                reverse_map = {"main": "Main (Back)", "ultrawide": "Ultrawide", "telephoto": "Telephoto", "front": "Front (Selfie)"}
                self._attr_current_option = reverse_map.get(lens, "Main (Back)")
        except requests.exceptions.RequestException:
            pass

    def select_option(self, option: str) -> None:
        lens_map = {"Main (Back)": "main", "Ultrawide": "ultrawide", "Telephoto": "telephoto", "Front (Selfie)": "front"}
        lens_param = lens_map.get(option, "main")
        try:
            requests.get(f"http://{self._ip}:{self._port}/lens?type={lens_param}", timeout=3)
            self._attr_current_option = option
        except requests.exceptions.RequestException:
            pass


class MSCamModeSelect(SelectEntity):
    def __init__(self, ip_address: str, http_port: int):
        self._attr_name = "MS IP Cam Operating Mode"
        self._attr_icon = "mdi:cog"
        self._attr_options = ["On-Demand", "Always On (24/7)"]
        self._attr_current_option = "On-Demand"
        self._ip = ip_address
        self._port = http_port

    @property
    def current_option(self) -> str:
        return self._attr_current_option

    def update(self):
        """Sync live mode selection from the phone app."""
        try:
            res = requests.get(f"http://{self._ip}:{self._port}/status", timeout=2)
            if res.status_code == 200:
                mode = res.json().get("mode", "on_demand")
                self._attr_current_option = "Always On (24/7)" if mode == "always_on" else "On-Demand"
        except requests.exceptions.RequestException:
            pass

    def select_option(self, option: str) -> None:
        mode_param = "always_on" if option == "Always On (24/7)" else "on_demand"
        try:
            requests.get(f"http://{self._ip}:{self._port}/mode?type={mode_param}", timeout=3)
            self._attr_current_option = option
        except requests.exceptions.RequestException:
            pass


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MSCamLensSelect(data["ip_address"], data["http_port"]),
        MSCamModeSelect(data["ip_address"], data["http_port"])
    ])
