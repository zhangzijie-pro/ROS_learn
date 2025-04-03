import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

class PubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name=node_name)
        self.get_logger().info(f"{node_name}---started now... ...")

        self.book_queue = Queue()
        self.book_publisher_ = self.create_publisher(String,"book", 10)
        self.create_timer(5, self.time_callback)


    def time_callback(self):
        if self.book_queue.qsize()>0:
            line = self.book_queue.get()
            msg = String()
            msg.data = line
            self.book_publisher_.publish(msg=msg)
            self.get_logger().info(f"publish : ----- {msg}")

    def download(self,url):
        response = requests.get(url)
        response.encoding="utf-8"
        result = response.text
        self.get_logger().info(f"download {url}...... \n get {len(result)}")
        for line in result.splitlines():
            if len(line)==0:
                continue
            self.book_queue.put(line)



def main():
    rclpy.init()
    node = PubNode("pub_node")
    node.download("http://0.0.0.0:8000/book1.txt")
    rclpy.spin(node)
    rclpy.shutdown()