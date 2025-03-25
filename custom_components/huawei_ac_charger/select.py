from homeassistant.components.select import SelectEntity

OPTIONS = {"Standby": 0, "Paused": 1, "Resume": 2}

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data["huawei_ac_charger"][entry.entry_id]["client"]
    async_add_entities([HuaweiChargingControl(client)])

class HuaweiChargingControl(SelectEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "Charging Control"
        self._attr_options = list(OPTIONS.keys())
        self._attr_current_option = "Standby"

    async def async_select_option(self, option):
        value = OPTIONS[option]
        await self._client.write_register(0x2006, value)
        self._attr_current_option = option