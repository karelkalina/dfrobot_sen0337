# Atom Lite DFRobot Distance Sensor

ESPHome firmware for an [M5Stack Atom Lite](https://docs.m5stack.com/en/core/ATOM%20Lite) with a [DFRobot SEN0337](https://wiki.dfrobot.com/TOF_Laser_Range_Finder_SKU_SEN0337) TOF laser distance sensor.

A local ESPHome external component reads the sensor's UART output and exposes distance (in meters) and signal strength as Home Assistant entities.

## Hardware

- **M5Stack Atom Lite** (ESP32-PICO-D4, 240MHz, 4MB flash)
- **DFRobot SEN0337** TOF laser distance sensor
  - TX: GPIO26
  - RX: GPIO32
  - Baud rate: 115200

## Prerequisites

- [pixi](https://pixi.sh) package manager

## Building and Flashing

```bash
# Install dependencies
pixi install

# Compile firmware
pixi run compile

# Compile, upload and show logs (device connected via USB)
pixi run run

# Upload pre-compiled firmware
pixi run upload

# View device logs
pixi run logs

# Clean build artifacts
pixi run clean
```

## WiFi Setup

On first boot (or when no saved WiFi network is available), the device starts a captive portal AP. Connect to it with your phone or laptop, then configure your WiFi credentials through the portal. The credentials are saved and used on subsequent boots.

The AP and captive portal should be also started if the device fails to connect to the saved WiFi network (e.g. due to network not available), after 90 seconds. You can use it to reconfigure WiFi settings.

The Improv via serial is also supported for WiFi configuration. To use it, connect to the serial port (provided via USB) and use [ESPHome Web](https://web.esphome.io/) tool to change WiFi settings.

## Sensors

Once connected to WiFi and Home Assistant, the device exposes:

- **Distance** — measured distance in meters (from SEN0337 TOF sensor)
- **Signal Strength** — signal strength of the TOF measurement

Additional diagnostic sensors (WiFi signal, uptime, heap free, etc.) are also available.

## Web Server

The device runs a web server on port 80 (`http://<device-ip>/`). It provides:

- Sensor readings (distance, signal strength)
- WiFi signal strength, IP address, SSID, and MAC address
- Device uptime
- Debug info (heap free, loop time, internal temperature)
- OTA firmware update capability

## Configuration

Main config: `atomlite-distance.yaml`

Local component: `components/dfrobot_sen0337/`

Shared packages in `packages/common/`: `wifi.yaml`, `uptime.yaml`, `debug.yaml`
