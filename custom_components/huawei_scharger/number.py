from homeassistant.components.number import NumberEntity
from pymodbus.client import ModbusTcpClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_DEBUG, UNIT_ID

class HuaweiSChargerMaxCurrent(NumberEntity):
    def __init__(self, name, address, host, port, debug):
        self._name = name
        self._address = address
        self._host = host
        self._port = port
        self._debug = debug
        self._attr_name = name
        self._attr_native_unit_of_measurement = "A"
        self._attr_native_min_value = 6
        self._attr_native_max_value = 32
        self._attr_native_step = 0.1
        self._attr_native_value = None

    def update(self):
        client = ModbusTcpClient(self._host, port=self._port, framer=ModbusRtuFramer)
        client.connect()
        rr = client.read_holding_registers(self._address, 1, unit=UNIT_ID)
        if not rr.isError():
            self._attr_native_value = rr.registers[0] * 0.1
            if self._debug:
                print(f"[HuaweiSCharger][DEBUG] Max Current: {rr.registers[0]}")
        client.close()

    def set_native_value(self, value: float):
        scaled = int(value * 10)
        client = ModbusTcpClient(self._host, port=self._port, framer=ModbusRtuFramer)
        client.connect()
        client.write_register(self._address, scaled, unit=UNIT_ID)
        client.close()

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    debug = entry.data.get(CONF_DEBUG, False)
    number = HuaweiSChargerMaxCurrent("Max Charging Current", 32003, host, port, debug)
    async_add_entities([number])