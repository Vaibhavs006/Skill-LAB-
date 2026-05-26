import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleChaserNode(Node):
    def __init__(self):
        super().__init__('turtle_chaser_node')
        self.velocity_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.chaser_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.update_chaser_pose, 10)
        self.target_subscriber = self.create_subscription(Pose, '/turtle2/pose', self.update_target_pose, 10)
        
        self.chaser_pose = Pose()
        self.target_pose = Pose()
        self.chaser_ready = False
        self.target_ready = False
        
        self.control_timer = self.create_timer(0.02, self.execute_chase)

    def update_chaser_pose(self, msg):
        self.chaser_pose = msg
        self.chaser_ready = True

    def update_target_pose(self, msg):
        self.target_pose = msg
        self.target_ready = True

    def execute_chase(self):
        if not self.chaser_ready or not self.target_ready:
            return

        command = Twist()
        delta_x = self.target_pose.x - self.chaser_pose.x
        delta_y = self.target_pose.y - self.chaser_pose.y
        
        distance = math.sqrt(delta_x**2 + delta_y**2)
        desired_angle = math.atan2(delta_y, delta_x)
        angle_error = desired_angle - self.chaser_pose.theta
        
        while angle_error > math.pi:
            angle_error -= 2.0 * math.pi
        while angle_error < -math.pi:
            angle_error += 2.0 * math.pi

        if distance > 0.6:
            command.linear.x = 1.2 * distance
            command.angular.z = 4.0 * angle_error
        else:
            command.linear.x = 0.0
            command.angular.z = 0.0

        self.velocity_publisher.publish(command)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleChaserNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
