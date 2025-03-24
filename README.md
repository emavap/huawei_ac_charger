
# Huawei AC Charger Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

This integration provides full Modbus-TCP support for Huawei AC Chargers.

## Features
- Real-time monitoring of charger parameters (voltage, current, power).
- Control charging state (standby, pause, resume).
- Set maximum charging power.
- Automatic Modbus TCP connection management.

## Installation
Install easily via [HACS](https://hacs.xyz/) by adding this repository as a custom integration.

## Configuration
Configure directly via Home Assistant integrations UI by entering the charger IP address and port (default 502).

## Entities Created
- Sensors for voltage, current, total power.
- Number entity to control maximum charging power.
- Select entity to control charging state.
- Connection status binary sensor.

## Contributions
Contributions are welcome via pull requests or issues.

## License
MIT
