from urllib.parse import urlparse
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "ms_ip_cam"
PLATFORMS = ["camera", "switch", "button", "select"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MS IP Cam from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    rtsp_url = entry.data["rtsp_url"]
    http_port = entry.data.get("http_port", 8080)
    
    # Automatically extract the IP Address from the RTSP URL
    parsed_url = urlparse(rtsp_url)
    ip_address = parsed_url.hostname or "192.168.1.100"

    hass.data[DOMAIN][entry.entry_id] = {
        "rtsp_url": rtsp_url,
        "ip_address": ip_address,
        "http_port": http_port
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
