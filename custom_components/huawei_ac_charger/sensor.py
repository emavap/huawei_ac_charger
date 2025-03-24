from homeassistant.components.sensor import SensorEntity
from .tcp_client import HuaweiTCPClient
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import logging

_LOGGER = logging.getLogger(__name__)

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
    
        request_frame = (
            b'\x00\x01\x00\x00\x00\x06\x01\x03' + 
            (0x1000).to_bytes(2, 'big') + b'\x00\x0E'  # reading multiple registers at once
        )
        response = await self._client.send_request(request_frame)
        
        _LOGGER.debug(f"Raw response for sensors: {response.hex()}")

        if response and len(response) >= 36:
            register_data = response[8:]  # Data starts explicitly from byte offset 8

            phase_l1_voltage = int.from_bytes(register_data[0:4], 'big') / 10000000
            phase_l2_voltage = int.from_bytes(register_data[4:8], 'big') / 10000000
            phase_l3_voltage = int.from_bytes(register_data[8:12], 'big') / 10000000
            phase_l1_current = int.from_bytes(register_data[12:16], 'big') / 10
            phase_l2_current = int.from_bytes(register_data[16:20], 'big') / 10
            phase_l3_current = int.from_bytes(register_data[20:24], 'big') / 10
            total_power = int.from_bytes(register_data[24:28], 'big') / 10

            # Assign values based on sensor name
            if self._attr_name == "Phase L1 Voltage":
                self._attr_native_value = phase_l1_voltage
            elif self._attr_name == "Phase L2 Voltage":
                self._attr_native_value = phase_l2_voltage
            elif self._attr_name == "Phase L3 Voltage":
                self._attr_native_value = phase_l3_voltage
            elif self._attr_name == "Phase L1 Current":
                self._attr_native_value = phase_l1_current
            elif self._attr_name == "Phase L2 Current":
                self._attr_native_value = phase_l2_current
            elif self._attr_name == "Phase L3 Current":
                self._attr_native_value = phase_l3_current
            elif self._attr_name == "Total Power":
                self._attr_native_value = total_power

            _LOGGER.debug(f"Parsed value for {self._attr_name}: {self._attr_native_value}")
        else:
            _LOGGER.error(f"Incomplete or invalid response received: {response}")
            self._attr_native_value = None