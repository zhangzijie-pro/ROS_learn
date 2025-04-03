import rclpy
from status_interface.msg import SystemStatus 
from rclpy.node import Node
import psutil
import platform

class StatusPub(Node):
    def __init__(self,node_name):
        super().__init__(node_name=node_name)
        self.publishers_ = self.create_publisher(SystemStatus, "SystemStatus",10)
        self.timer_ = self.create_timer(1.0,self.timer_callback)


    def timer_callback(self):
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        net_io_count = psutil.net_io_counters()

        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.host_name = platform.node()
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total/1024/1024
        msg.memory_available = memory_info.available/1024/1024
        msg.net_sent = net_io_count.bytes_sent/1024/1024
        msg.net_recv = net_io_count.bytes_recv/1024/1024

        self.get_logger().info(f"发布:{str(msg)}")

        self.publishers_.publish(msg=msg)

def main():
    rclpy.init()
    node = StatusPub("sys_status_pub")
    rclpy.spin(node)
    rclpy.shutdown()
