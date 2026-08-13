import requests
from homeassistant.components.select import SelectEntity

ANDROID_IP = "192.168.1.100"  # Replace with your phone's local IP address

class MSCamModeSelect(SelectEntity):
    def __init__(self):
        self._attr_name = "MS IP Cam Operating Mode"
        self._attr_options = ["On-Demand", "Always On (24/7)"]
        self._attr_current_option = "On-Demand"

    @property
    def name(self):
        return self._attr_name

    @property
    def current_option(self) -> str:
        return self._attr_current_option

    def select_option(self, option: str) -> None:
        """Handle mode changes from Home Assistant UI."""
        mode_param = "always_on" if option == "Always On (24/7)" else "on_demand"
        try:
            requests.get(f"http://{ANDROID_IP}:8080/mode?type={mode_param}", timeout=3)
            self._attr_current_option = option
        except requests.exceptions.RequestException:
            pass

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([MSCamModeSelect()])
