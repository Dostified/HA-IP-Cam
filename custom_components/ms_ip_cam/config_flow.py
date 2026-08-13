import voluptuous as vol
import aiohttp
from urllib.parse import urlparse
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = "ms_ip_cam"

class MSIPCamConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for MS IP Cam."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            rtsp_url = user_input["rtsp_url"]
            http_port = user_input["http_port"]
            
            parsed_url = urlparse(rtsp_url)
            ip_address = parsed_url.hostname
            
            if not ip_address:
                errors["base"] = "invalid_rtsp_url"
            else:
                try:
                    # Validate connection to the app before saving
                    session = async_get_clientsession(self.hass)
                    async with session.get(
                        f"http://{ip_address}:{http_port}/status", 
                        timeout=5
                    ) as response:
                        if response.status == 200:
                            user_input["ip_address"] = ip_address
                            return self.async_create_entry(
                                title=f"MS IP Cam ({ip_address})", 
                                data=user_input
                            )
                        else:
                            errors["base"] = "cannot_connect"
                except Exception:
                    errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(
                "rtsp_url", 
                default="rtsp://admin:admin123@192.168.1.100:8554/live"
            ): str,
            vol.Required("http_port", default=8080): int,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
