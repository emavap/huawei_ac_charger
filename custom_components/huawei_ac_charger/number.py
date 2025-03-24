from homeassistant.components.number import NumberEntity

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data["huawei_ac_charger"][entry.entry_id]["client"]
    async_add_entities([HuaweiMaxChargingPower(client)])

class HuaweiMaxChargingPower(NumberEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "Max Charging Power"
        self._attr_native_unit_of_measurement = "kW"
        self._attr_min_value = 0
        self._attr_max_value = 22

    async def async_set_native_value(self, value):
        scaled_value = int(value * 10)
        await self._client.write_registers(0x2000, scaled_value.to_bytes(4, 'big'))