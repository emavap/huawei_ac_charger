from homeassistant.components.sensor import SensorEntity
from .tcp_client import HuaweiTCPClient
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    client: HuaweiTCPClient = hass.data["huawei_ac_charger"][entry.entry_id]["client"]
    sensors = [
        ("Phase L1 Voltage", "V", 0x1000),
        ("Phase L2 Voltage", "V", 0x1002),
        ("Phase L3 Voltage", "V", 0x1004),
        ("Total Power", "kW", 0x100C)
    ]
    entities = [HuaweiSensor(client, name, unit, address) for name, unit, address in sensors]
    async_add_entities(entities, update_before_add=True)

class HuaweiSensor(SensorEntity):
    def __init__(self, client, name, unit, address):
        self._client = client
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._address = address

    async def async_update(self):
        request_frame = b'\\x00\\x01\\x00\\x00\\x00\\x06\\x01\\x03' + self._address.to_bytes(2, 'big') + b'\\x00\\x02'
        response = await self._client.send_request(request_frame)
        if response and len(response) >= 9:
            self._attr_native_value = int.from_bytes(response[9:13], 'big') / 10
        else:
            self._attr_native_value = None