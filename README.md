# SEN0337 Distance Sensor

This repository contains the configuration and ROS 2 driver for the SEN0337 distance sensor.

## Directory Structure
- `firmware/`: Contains the ESPHome configuration (`atomlite-distance.yaml`) and related files for the [Atom Lite board](https://shop.m5stack.com/products/atom-lite-esp32-development-kit) to the [SEN0337 sensor](https://wiki.dfrobot.com/TOF_Laser_Range_Finder_SKU_SEN0337).

- `ros_node/`: Contains the `sen0337_driver` ROS 2 package to interface with the sensor over HTTP.

## Sensor Wiring

| Color  | Label | Description                       | Atom Lite |
| ------ | ----- | --------------------------------- | --------- |
| Red    | VCC   | power supply input positive pole  | 5V        |
| Black  | GND   | power ground wire                 | GND       |
| Yellow | RXD   | UART TTL receive line             | GPIO26    |
| White  | TXD   | UART TTL transmit line            | GPIO32    |

Wiring connection via jumper cable to [M5 Grove Cable](https://docs.m5stack.com/en/accessory/cable/grove_cable):
- Red (Sensor) -> Red -> Red (Grove)
- Black (Sensor) -> Brown -> Black (Grove)
- Blue (Sensor) -> Yellow -> Yellow (Grove)
- Green (Sensor) -> White -> White (Grove)

For reference, see [Atom Lite Documentation](https://docs.m5stack.com/en/core/Atom-Lite) and [SEN0337 Wiki](https://wiki.dfrobot.com/TOF_Laser_Range_Finder_SKU_SEN0337).

## Build and Flash Instructions

```bash
pixi run compile
pixi run upload
```

## Network Configuration

The sensor is configured to use a static IP address (`192.168.105.67`) on a
private network, which credentials must be set in `firmware/secrets.yaml`.
To switch to a different network, update the `secrets.yaml` and provide Wi-Fi
credentials or use the ESPHome captive portal that will be available when the
device cannot connect to the configured network.

Format of `secrets.yaml`:
```yaml
wifi_ssid: "YourWiFiSSID"
wifi_password: "YourWiFiPassword"
```

## ROS 2 Node

The corresponding ROS 2 node for this sensor is `sen0337_node`. It polls the
ESPHome web server to retrieve distance measurements and publishes them as a
`sensor_msgs/Range` message.

- **Default IP:** `192.168.105.67`
- **ESPHome Endpoint:** `/text_sensor/paired_sensor_data`
- **Output Topic:** `/sen0337/distance` (Range in meters)
- **Frame ID:** `sen0337_link`

### Usage

Run the node using:
```bash
source <ROS Workspace>/install/setup.bash
ros2 run sen0337_driver sen0337_node --ros-args -p sensor_ip:=192.168.105.67
```

# Setup instruction
1. (Recommended, not necessary) Connect the M5 Atom Lite to a pc and flash it with the factory firmware
2. Go to 'web.esphome.io', and connect to your desired wifi network. Check the device ip and modify 'firmware/atomlite-distance.yaml' and 'ros_node/sen0337_driver/sen0337_driver/sen0337_node.py' to reflect this
3. Compile and run the firmware using pixi (from `firmware/` directory)
```bash
pixi run compile
pixi run upload --device {ip_address}
```
4. Verify that the device runs properly, either by checking the web server, endpoint or ros node (if something isn't working, I recommend debugging in this order)
