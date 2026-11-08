import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_DISTANCE,
    CONF_SIGNAL_STRENGTH,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    STATE_CLASS_MEASUREMENT,
    UNIT_METER,
)

from . import DFRobotSEN0337Component, dfrobot_sen0337_ns

CONF_DFROBOT_SEN0337_ID = "dfrobot_sen0337_id"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_DFROBOT_SEN0337_ID): cv.use_id(DFRobotSEN0337Component),
        cv.Optional(CONF_DISTANCE): sensor.sensor_schema(
            unit_of_measurement=UNIT_METER,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_DISTANCE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_SIGNAL_STRENGTH): sensor.sensor_schema(
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_DFROBOT_SEN0337_ID])

    if distance_config := config.get(CONF_DISTANCE):
        sens = await sensor.new_sensor(distance_config)
        cg.add(parent.set_distance_sensor(sens))

    if signal_config := config.get(CONF_SIGNAL_STRENGTH):
        sens = await sensor.new_sensor(signal_config)
        cg.add(parent.set_signal_strength_sensor(sens))
