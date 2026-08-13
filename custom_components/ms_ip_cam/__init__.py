from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "ms_ip_cam"
PLATFORMS = ["camera", "switch", "select"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MS IP Cam from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    # Store the user's IP address and Port in HA's memory
    hass.data[DOMAIN][entry.entry_id] = entry.data 
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
