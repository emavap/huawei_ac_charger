from .tcp_client import HuaweiTCPClient

PLATFORMS = ["sensor"]

async def async_setup_entry(hass, entry):
    client = HuaweiTCPClient(entry.data["ip_address"], entry.data["port"])
    await client.connect()
    hass.data.setdefault("huawei_ac_charger", {})[entry.entry_id] = {"client": client}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
