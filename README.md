# Huawei SCharger Home Assistant Integration

This custom integration connects Home Assistant to a Huawei SCharger using Modbus RTU over TCP.

- Reads real-time power, voltage, and current
- Enables/disables charging
- Adjusts maximum charging current

## Installation via HACS

1. Go to HACS → Integrations → Menu (⋮) → Custom repositories
2. Add this repo URL and select 'Integration'
3. Search for 'Huawei SCharger' in HACS and install

## Configuration
Use the Home Assistant UI to configure IP, port, and optional debug logging.