from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    sensors = [
        ("Phase L1 Voltage", "V", 0x1000),
        ("Phase L2 Voltage", "V", 0x1002),
        ("Phase L3 Voltage", "V", 0x1004),
        ("Total Power", "kW", 0x100C)
    ]
    client = hass.data["huawei_ac_charger"][entry.entry_id]["client"]
    entities = [HuaweiSensor(client, name, unit, addr) for name, unit, addr in sensors]
    async_add_entities(entities)

class HuaweiSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, client, name, unit, address):
        super().__init__(None)
        self._client = client
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._address = address

    async def async_update(self):
        result = await self._client.read_holding_registers(self._address, 2)
        if result.isError():
            self._attr_native_value = None
        else:
            self._attr_native_value = int.from_bytes(result.registers, "big") / 10