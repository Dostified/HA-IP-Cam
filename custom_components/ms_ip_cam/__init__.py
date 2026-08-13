from homeassistant.core import HomeAssistant

DOMAIN = "ms_ip_cam"

def setup(hass: HomeAssistant, config: dict) -> bool:
    hass.helpers.discovery.load_platform("camera", DOMAIN, {}, config)
    hass.helpers.discovery.load_platform("switch", DOMAIN, {}, config)
    hass.helpers.discovery.load_platform("select", DOMAIN, {}, config)
    return True
