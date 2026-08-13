from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

DOMAIN = "ha_ip_camera"
PLATFORMS = ["camera", "switch", "select"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Home Assistant IP Camera from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    rtsp_url = entry.data["rtsp_url"]
    http_port = entry.data.get("http_port", 8080)
    
    # Robust IP extraction from RTSP URL if not explicitly provided
    if "ip_address" in entry.data:
        ip_address = entry.data["ip_address"]
    else:
        import re
        # Matches IP address in various RTSP URL formats
        match = re.search(r'@?([\d\.]+):?\d*/', rtsp_url)
        if match:
            ip_address = match.group(1)
        else:
            # Fallback for URLs without path
            match = re.search(r'@?([\d\.]+):?\d*$', rtsp_url)
            ip_address = match.group(1) if match else "0.0.0.0"

    hass.data[DOMAIN][entry.entry_id] = {
        "rtsp_url": rtsp_url,
        "ip_address": ip_address,
        "http_port": http_port
    }

    # Register the device
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name=f"Home Assistant IP Camera ({ip_address})",
        manufacturer="Mukesh Saw",
        model="Android IP Camera",
        sw_version="2.0.0",
    )
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
