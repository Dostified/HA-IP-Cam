from homeassistant.core import HomeAssistant

DOMAIN = "my_pro_cam"

def setup(hass: HomeAssistant, config: dict) -> bool:
    hass.helpers.discovery.load_platform("camera", DOMAIN, {}, config)
    hass.helpers.discovery.load_platform("switch", DOMAIN, {}, config)
    return True
