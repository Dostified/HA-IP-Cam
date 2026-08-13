import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "ms_ip_cam"

class MSIPCamConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MS IP Cam."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Save the IP address the user typed in!
            return self.async_create_entry(title="MS IP Cam", data=user_input)

        # Show the form to the user
        data_schema = vol.Schema({
            vol.Required("ip_address", default="192.168.1.100"): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema
        )
