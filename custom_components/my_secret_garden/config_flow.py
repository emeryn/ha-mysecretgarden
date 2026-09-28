import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_API_URL

class MySecretGardenConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gère la configuration via l'interface UI."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Mon Potager", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_URL, default="http://192.168.1.XX:8000"): str
            })
        )
