#!/usr/bin/env python3
import requests
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

class SEN0337Node(Node):
    def __init__(self):
        super().__init__('sen0337_node')
        self.declare_parameter('sensor_ip', '192.168.105.67')
        self.declare_parameter('frame_id', 'sen0337_link')
        self.declare_parameter('poll_period', 0.1)

        self.sensor_ip = self.get_parameter('sensor_ip').get_parameter_value().string_value
        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        poll_period = self.get_parameter('poll_period').get_parameter_value().double_value

        self.url = f'http://{self.sensor_ip}/text_sensor/paired_sensor_data'
        self.publisher_ = self.create_publisher(Range, '/sen0337/distance', 10)
        self.timer = self.create_timer(poll_period, self.timer_callback)

        self.get_logger().info(f'SEN0337 node started: {self.url}')

    def timer_callback(self):
        try:
            response = requests.get(self.url, timeout=(1.0, 2.0))
            response.raise_for_status()
            data = response.json()  
            distance_m = float(data['value'])

            msg = Range()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            msg.radiation_type = Range.INFRARED
            msg.field_of_view = 0.1
            msg.min_range = 0.0
            msg.max_range = 10.0
            msg.range = distance_m

            self.publisher_.publish(msg)
        except Exception as e:
            self.get_logger().warn(f'Error: {e}', throttle_duration_sec=2.0)

def main(args=None):
    rclpy.init(args=args)
    node = SEN0337Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
