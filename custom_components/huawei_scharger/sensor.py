from homeassistant.components.sensor import SensorEntity
from homeassistant.const import POWER_WATT
from pymodbus.client import ModbusTcpClient
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_DEBUG, UNIT_ID

SENSORS = [
    ("Charging Power", 32064, 2, POWER_WATT, "power"),
    ("Charging Voltage", 32066, 1, "V", "voltage"),
]

async def async_setup_entry(hass, entry, async_add_entities):
    sensors = []
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    debug = entry.data.get(CONF_DEBUG, False)

    for name, reg, count, unit, key in SENSORS:
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
        self._attr_native_unit_of_measurement = unit
        self._attr_native_value = None

    def update(self):
        client = ModbusTcpClient(self._host, port=self._port)
        client.connect()
        rr = client.read_holding_registers(self._register, self._count, unit=UNIT_ID)
        if not rr.isError():
            if self._count == 2:
                value = (rr.registers[0] << 16) + rr.registers[1]
            else:
                value = rr.registers[0]
            self._attr_native_value = value
            if self._debug:
                print(f"[HuaweiSCharger][DEBUG] {self._name}: {value}")
        client.close()