from .modbus_rtu_tcp import build_rtu_frame, build_write_frame, send_rtu_tcp
from homeassistant.components.sensor import SensorEntity
from .tcp_client import HuaweiTCPClient
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data["huawei_ac_charger"][entry.entry_id]["client"]
    sensors = [
        ("Phase L1 Voltage", "V"),
        ("Phase L2 Voltage", "V"),
        ("Phase L3 Voltage", "V"),
        ("Phase L1 Current", "A"),
        ("Phase L2 Current", "A"),
        ("Phase L3 Current", "A"),
        ("Total Power", "W")
    ]
    async_add_entities([HuaweiSensor(client, name, unit, idx) for idx, (name, unit) in enumerate(sensors)], update_before_add=True)

class HuaweiSensor(SensorEntity):
    def __init__(self, client, name, unit, index):
        self._client = client
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._index = index

    async def async_update(self):
        request = b'\x00\x01\x00\x00\x00\x06\x01\x03\x10\x00\x00\x0E'
        response = await self._client.send_request(request)

        if response:
            try:
                _LOGGER.debug(f"Raw response for {self._attr_name}: {response.hex()}")
                data = response[9 + self._index * 4 : 13 + self._index * 4]
                value = int.from_bytes(data, 'big')
                if self._attr_native_unit_of_measurement == "V":
                    self._attr_native_value = round(value / 10_000_000, 2)
                elif self._attr_native_unit_of_measurement == "A":
                    self._attr_native_value = round(value / 10, 2)
                elif self._attr_native_unit_of_measurement == "W":
                    self._attr_native_value = round(value / 10, 2)
            except Exception as e:
                _LOGGER.error(f"Failed to parse sensor {self._attr_name}: {e}")
                self._attr_native_value = None
        else:
            _LOGGER.error(f"No response received for {self._attr_name}")
            self._attr_native_value = None
