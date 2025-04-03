import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node("python_node")
    node.get_logger().info("this is a info log")
    rclpy.spin(node=node)
    rclpy.shutdown()

if __name__=='__main__':
    main()