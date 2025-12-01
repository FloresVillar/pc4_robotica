import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class MoverBrazo(Node):
    def __init__(self):
        super().__init__('mover_brazo')
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)

        # Nombres de las articulaciones
        self.joint_names = ['joint1', 'joint2']

        # Amplitud máxima de giro para cada joint (radianes)
        self.amplitudes = [math.pi/4, math.pi/6]  # joint1 = 45°, joint2 = 30°

        # Velocidad angular (rad/s)
        self.speeds = [1.0, 1.5]

        # Timer para actualizar posición 20 veces por segundo
        self.timer = self.create_timer(0.05, self.mover)

        # Tiempo inicial
        self.start_time = self.get_clock().now().nanoseconds * 1e-9

    def mover(self):
        # Tiempo actual
        t = self.get_clock().now().nanoseconds * 1e-9 - self.start_time

        # Calcular ángulos usando función seno para movimiento suave
        angles = [
            self.amplitudes[0] * math.sin(self.speeds[0] * t),
            self.amplitudes[1] * math.sin(self.speeds[1] * t)
        ]

        # Crear mensaje JointState
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = angles

        # Publicar en /joint_states
        self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoverBrazo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
