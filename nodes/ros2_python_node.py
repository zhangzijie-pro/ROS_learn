import rclpy
from rclpy.node import Node

def main():
    rclpy.init()    # 初始化,分配资源
    node = Node("python_node")
    node.get_logger().info("hello, this is python node")
    node.get_logger().warn("this is a warning log")
    node.get_logger().error("this is a error log")

    rclpy.spin(node=node)   # 开启节点
    rclpy.shutdown()

if __name__== '__main__':
    main()