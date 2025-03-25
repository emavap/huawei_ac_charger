# Huawei SCharger Integration for Home Assistant

This custom integration enables Home Assistant to communicate with Huawei SChargers using Modbus RTU over TCP.

## Features
- Enable/disable charging
- Monitor charging power and voltage
- Set max charging current
- Works with FramerRTU-compatible pymodbus versions (e.g., 2.5.x)
- Configurable via Home Assistant UI

## Installation

### Manual
1. Copy `custom_components/huawei_scharger` into your Home Assistant `config/custom_components` folder.
2. Restart Home Assistant.

### HACS (Recommended)
1. In HACS, go to **Integrations → ⋮ → Custom repositories**
2. Add your GitHub repo URL and select category "Integration"
3. Search for "Huawei SCharger" and install

## Configuration
1. Go to Home Assistant **Settings → Devices & Services**
2. Add "Huawei SCharger" and enter the IP address, port, and enable debug if needed.