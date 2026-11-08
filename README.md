# SEN0337 Distance Sensor

This repository contains the configuration and ROS 2 driver for the SEN0337 distance sensor.

## Directory Structure
- `firmware/`: Contains the ESPHome configuration (`atomlite-distance.yaml`) and related files.
- `ros_node/`: Contains the `sen0337_driver` ROS 2 package to interface with the sensor over HTTP.

## Network Configuration
- **Static IP:** `192.168.105.67`

# Setup instruction
1. (Recommended, not necessary) Connect the M5 Atom Lite to a pc and flash it with the factory firmware
2. Go to 'web.esphome.io', and connect to your desired wifi network. Check the device ip and modify 'firmware/atomlite-distance.yaml' and 'ros_node/sen0337_driver/sen0337_driver/sen0337_node.py' to reflect this
3. Compile and run the firmware using pixi (from `firmware/` directory)
```bash
pixi run compile
pixi run upload --device {ip_address}
```
4. Verify that the device runs properly, either by checking the web server, endpoint or ros node (if something isn't working, I recommend debugging in this order)

# Wiring
- For wiring instructions see 'https://docs.m5stack.com/en/core/Atom-Lite' and 'https://wiki.dfrobot.com/sen0337/#tech_specs'
    
    sensor -> jumper cable -> cable m5

    black -> brown -> black
    red -> red -> red
    blue -> yellow -> yellow
    green -> white -> white

    cable : 'https://docs.m5stack.com/en/accessory/cable/grove_cable'