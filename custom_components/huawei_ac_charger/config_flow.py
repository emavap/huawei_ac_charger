import voluptuous as vol
from homeassistant import config_entries

class HuaweiConfigFlow(config_entries.ConfigFlow, domain="huawei_ac_charger"):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Huawei Charger", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("ip_address"): str,
                vol.Required("port", default=502): int,
            }),
        )