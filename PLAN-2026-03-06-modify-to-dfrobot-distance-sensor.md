# Plan: Atom Lite + DFRobot SEN0337 Distance Sensor

## Context

The project currently runs on M5Stack CoreS3 as a serial-to-TCP bridge using the `stream_server` external component. We need to repurpose it for an **M5Stack Atom Lite** board with a **DFRobot SEN0337 TOF laser distance sensor** connected via UART. Instead of bridging serial to TCP, we'll write a custom ESPHome component that parses the sensor's UART frames and exposes distance data natively to ESPHome/Home Assistant.

## SEN0337 UART Protocol (from official Arduino example)

- **Baud rate:** 115200
- **Mode:** Active output — sensor continuously sends 16-byte frames
- **Frame format (16 bytes):**
  - Bytes 0-3: Header `0x57 0x00 0xFF 0x00`
  - Bytes 4-7: System time (uint32 LE, ms)
  - Bytes 8-9: Distance (uint16 LE, millimeters)
  - Byte 10: (unused/extended distance byte)
  - Byte 11: Distance status (0 = valid)
  - Bytes 12-13: Signal strength (uint16 LE)
  - Byte 14: Range precision
  - Byte 15: Checksum (sum of bytes 0-14 & 0xFF)

## Approach

Single approach — create a local ESPHome external component:

### 1. Rename main YAML config

- Rename `cores3-serialserver.yaml` → `atomlite-distance.yaml`
- Change board to `m5stack-atom` (ESP32-PICO-D4)
- Remove: `external_components` (stream_server + M5CoreS3), `board_m5cores3`, `psram`, M5 libraries, `stream_server` config, baud rate select, stream_server sensors
- Change UART to GPIO26 (TX) / GPIO32 (RX) at 115200 baud
- Add local external component reference: `source: components`
- Add `dfrobot_sen0337` component config with sensor definitions
- Keep: wifi, captive_portal, improv_serial, logger, api, ota, web_server, common packages

### 2. Create local component: `components/dfrobot_sen0337/`

**Files to create:**

#### `components/dfrobot_sen0337/__init__.py`
- Declare `DFRobotSEN0337Component` class (inherits `Component`)
- `DEPENDENCIES = ["uart"]`
- Extend `uart.UART_DEVICE_SCHEMA`
- Register as UART device in `to_code()`

#### `components/dfrobot_sen0337/sensor.py`
- Define optional sensor configs: `distance`, `signal_strength`
- Wire sensors to C++ setters

#### `components/dfrobot_sen0337/dfrobot_sen0337.h`
- Class inheriting `esphome::Component` + `esphome::uart::UARTDevice`
- Sensor pointer members for distance and signal strength
- Frame buffer (16 bytes), parse state tracking
- `setup()`, `loop()`, `dump_config()` overrides

#### `components/dfrobot_sen0337/dfrobot_sen0337.cpp`
- `loop()`: read available bytes, scan for header `0x57 0x00 0xFF 0x00`
- Once 16 bytes collected after header match: verify checksum, parse fields
- Publish distance (mm converted to m as float) and signal strength
- Log warnings on checksum failures or invalid status
- Throttle publishing to avoid flooding (publish latest valid reading)

### 3. Update `CLAUDE.md` and `README.md`

Reflect new board, sensor, and component architecture.

## File Changes Summary

| File | Action |
|------|--------|
| `cores3-serialserver.yaml` | Delete |
| `atomlite-distance.yaml` | Create (new main config) |
| `components/dfrobot_sen0337/__init__.py` | Create |
| `components/dfrobot_sen0337/sensor.py` | Create |
| `components/dfrobot_sen0337/dfrobot_sen0337.h` | Create |
| `components/dfrobot_sen0337/dfrobot_sen0337.cpp` | Create |
| `CLAUDE.md` | Update |
| `README.md` | Update |

Common packages (`packages/common/wifi.yaml`, `uptime.yaml`, `debug.yaml`) remain unchanged.

## Key Design Decisions

- **Local component** (`source: components`) — no external GitHub dependency, lives in repo
- **Active mode only** — sensor pushes data, we just parse; no query commands needed
- **Distance in meters** — raw mm from sensor divided by 1000, standard for HA distance sensors
- **Checksum validation** — drop frames with bad checksum, log warning
- **No `CONFIG_ARDUINO_LOOP_STACK_SIZE` override** — Atom Lite has simpler setup, default should suffice
- **115200 baud** — matches official DFRobot Arduino example

## Verification

1. `pixi run compile` — must succeed with no errors
2. `pixi run run` (with device connected) — check logs for:
   - Sensor initialization message
   - Distance readings being published
   - No checksum errors with sensor connected
3. Home Assistant — verify distance and signal strength entities appear
