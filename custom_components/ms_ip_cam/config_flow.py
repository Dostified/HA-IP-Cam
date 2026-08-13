import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "ms_ip_cam"

class MSIPCamConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for MS IP Cam."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="MS IP Cam", data=user_input)

        data_schema = vol.Schema({
            vol.Required(
                "rtsp_url", 
                default="rtsp://admin:admin123@192.168.1.100:8554/live"
            ): str,
            vol.Required("http_port", default=8080): int,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema
        )
