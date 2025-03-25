from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_DEBUG

class HuaweiSChargerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Huawei SCharger", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default="192.168.5.118"): str,
                vol.Required(CONF_PORT, default=502): int,
                vol.Optional(CONF_DEBUG, default=False): bool,
            })
        )