from homeassistant.components.binary_sensor import BinarySensorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data["huawei_ac_charger"][entry.entry_id]["client"]
    async_add_entities([HuaweiConnectionSensor(client)], update_before_add=True)

class HuaweiConnectionSensor(BinarySensorEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "Connection Status"

    async def async_update(self):
        self._attr_is_on = self._client.connected