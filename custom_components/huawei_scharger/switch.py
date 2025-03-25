from homeassistant.components.switch import SwitchEntity
from pymodbus.client import ModbusTcpClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_DEBUG, UNIT_ID

class HuaweiSChargerSwitch(SwitchEntity):
    def __init__(self, name, address, host, port, debug):
        self._name = name
        self._address = address
        self._host = host
        self._port = port
        self._debug = debug
        self._attr_is_on = None
        self._attr_name = name

    def update(self):
        client = ModbusTcpClient(self._host, port=self._port, framer=ModbusRtuFramer)
        client.connect()
        rr = client.read_holding_registers(self._address, 1, unit=UNIT_ID)
        if not rr.isError():
            self._attr_is_on = rr.registers[0] == 1
            if self._debug:
                print(f"[HuaweiSCharger][DEBUG] Enable state: {rr.registers[0]}")
        client.close()

    def turn_on(self, **kwargs):
        client = ModbusTcpClient(self._host, port=self._port, framer=ModbusRtuFramer)
        client.connect()
        client.write_register(self._address, 1, unit=UNIT_ID)
        client.close()

    def turn_off(self, **kwargs):
        client = ModbusTcpClient(self._host, port=self._port, framer=ModbusRtuFramer)
        client.connect()
        client.write_register(self._address, 0, unit=UNIT_ID)
        client.close()

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    debug = entry.data.get(CONF_DEBUG, False)
    switch = HuaweiSChargerSwitch("Charger Enable", 32002, host, port, debug)
    async_add_entities([switch])