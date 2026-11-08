# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ESPHome firmware for an M5Stack Atom Lite (ESP32-PICO-D4) with a DFRobot SEN0337 TOF laser distance sensor connected via UART. A local ESPHome external component parses the sensor's 16-byte UART frames and exposes distance and signal strength as native ESPHome/Home Assistant sensors.

## Build Commands

All commands use [pixi](https://pixi.sh) as the package manager (ESPHome 2025.12.7 via PyPI):

```bash
pixi install        # Install dependencies (first time only)
pixi run compile   # Compile firmware
pixi run run       # Compile + upload + show logs (USB connected)
pixi run upload    # Upload pre-compiled firmware
pixi run logs      # Stream device logs
pixi run clean     # Clean build artifacts
```

After any YAML change, run `pixi run compile` to verify correctness.

## Architecture

**Main config:** `atomlite-distance.yaml` — contains all device-specific configuration.

**Local external component** in `components/dfrobot_sen0337/`:
- `__init__.py` — component registration, UART device schema
- `sensor.py` — sensor platform config (distance, signal strength)
- `dfrobot_sen0337.h` — C++ header (component class declaration)
- `dfrobot_sen0337.cpp` — C++ implementation (frame parsing, checksum validation, publishing)

**Reusable packages** in `packages/common/` are included via `!include`:
- `wifi.yaml` — WiFi info sensors (IP, SSID, MAC, signal strength, scan results)
- `uptime.yaml` — uptime sensor with human-readable text conversion
- `debug.yaml` — heap free, loop time, internal temperature, ESPHome version

## Integrations

- **web_server** (port 80) — device dashboard with status and OTA update
- **api** — Home Assistant native API (reboot timeout disabled)
- **ota** — over-the-air firmware updates via ESPHome
- **captive_portal** — WiFi provisioning AP on first boot / when no network is saved
- **improv_serial** — WiFi provisioning via USB serial (used by ESPHome web dashboard)

## Key Design Decisions

- **Local component** (`source: components`) — no external GitHub dependency, lives in repo
- **Active mode only** — SEN0337 continuously sends 16-byte frames; component just parses, no query commands
- **Distance in meters** — raw mm from sensor divided by 1000, standard for HA distance sensors
- **Checksum validation** — frames with bad checksum are dropped with a log warning
- **No `secrets.yaml`** — WiFi is configured at runtime via captive portal, not hardcoded
- **`name_add_mac_suffix: true`** — allows multiple devices with the same firmware
- **Logger uses USB CDC serial** — does not conflict with sensor UART on GPIO26/32

## SEN0337 UART Protocol

- Baud rate: 115200, active output mode (sensor pushes 16-byte frames)
- Header: `0x57 0x00 0xFF 0x00`
- Distance: bytes 8-9 (uint16 LE, mm), status: byte 11 (0 = valid)
- Signal strength: bytes 12-13 (uint16 LE)
- Checksum: byte 15 (sum of bytes 0-14 & 0xFF)

## Hardware Pin Mapping

- UART TX: GPIO26, RX: GPIO32 (DFRobot SEN0337 on Atom Lite Grove port)
