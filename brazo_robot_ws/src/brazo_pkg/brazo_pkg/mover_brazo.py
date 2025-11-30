import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class MoverBrazo(Node):
    def __init__(self):
        super().__init__('mover_brazo')
        self.pub = self.create_publisher(Float64, '/joint1_position_controller/command', 10)
        self.timer = self.create_timer(1.0, self.mover)
        self.angle = 0.0

    def mover(self):
        msg = Float64()
        msg.data = self.angle
        self.pub.publish(msg)
        self.angle += 0.1  # gira un poco cada segundo

rclpy.init()
node = MoverBrazo()
rclpy.spin(node)
