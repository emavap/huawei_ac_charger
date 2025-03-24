
from .tcp_client import HuaweiTCPClient

PLATFORMS = ["sensor", "number", "select", "binary_sensor"]

async def async_setup_entry(hass, entry):
    hass.data.setdefault("huawei_ac_charger", {})
    client = HuaweiTCPClient(entry.data["ip_address"], entry.data["port"])
    await client.connect()
    hass.data["huawei_ac_charger"][entry.entry_id] = {"client": client}
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )
    return True
