from homeassistant.components.sensor import SensorEntity
from homeassistant.const import POWER_WATT, ELECTRIC_POTENTIAL_VOLT
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.framer.rtu_framer import FramerRTU
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_DEBUG, UNIT_ID

SENSORS = [
    ("Charging Power", 32064, 2, POWER_WATT),
    ("Charging Voltage", 32066, 1, ELECTRIC_POTENTIAL_VOLT),
]

async def async_setup_entry(hass, entry, async_add_entities):
    sensors = []
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    debug = entry.data.get(CONF_DEBUG, False)

    for name, reg, count, unit in SENSORS:
        sensors.append(HuaweiSChargerSensor(name, reg, count, unit, host, port, debug))

    async_add_entities(sensors)

class HuaweiSChargerSensor(SensorEntity):
    def __init__(self, name, register, count, unit, host, port, debug):
        self._name = name
        self._register = register
        self._count = count
        self._unit = unit
        self._host = host
        self._port = port
        self._debug = debug
        self._attr_name = name
        self._attr_unit_of_measurement = unit
        self._state = None

    def update(self):
        client = ModbusTcpClient(self._host, port=self._port, framer=FramerRTU)
        client.connect()
        rr = client.read_holding_registers(self._register, self._count, unit=UNIT_ID)
        if not rr.isError():
            self._state = (rr.registers[0] << 16) + rr.registers[1] if self._count == 2 else rr.registers[0]
            if self._debug:
                print(f"[HuaweiSCharger][DEBUG] {self._name}: {self._state}")
        client.close()

    @property
    def native_value(self):
        return self._state