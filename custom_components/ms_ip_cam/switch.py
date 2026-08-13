from homeassistant.components.switch import SwitchEntity
import requests

ANDROID_IP = "192.168.1.100"

class FlashlightSwitch(SwitchEntity):
    def __init__(self):
        self._attr_name = "Android Camera Flashlight"
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        try:
            requests.get(f"http://{ANDROID_IP}:8080/flash?state=on", timeout=3)
            self._is_on = True
        except requests.exceptions.RequestException:
            pass

    def turn_off(self, **kwargs):
        try:
            requests.get(f"http://{ANDROID_IP}:8080/flash?state=off", timeout=3)
            self._is_on = False
        except requests.exceptions.RequestException:
            pass

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([FlashlightSwitch()])