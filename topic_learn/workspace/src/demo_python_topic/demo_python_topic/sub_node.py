import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class SubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.book_queue = Queue()
        self.book_subscription_ = self.create_subscription(String, "book", 
                                                           self.book_callback,10)
        
        self.get_logger().info(f"{node_name}---started now... ...")
        self.speech_threading_ = threading.Thread(target=self.speak_thread)
        self.speech_threading_.start()

    def book_callback(self,msg):
        self.get_logger().info(f"get: --> {msg}")
        self.book_queue.put(msg)

    def speak_thread(self):
        speaker = espeakng.Speaker()
        speaker.voice="zh"

        while rclpy.ok():
            if self.book_queue.qsize() > 0:
                text = self.book_queue.get()
                self.get_logger().info(f"speak: --> {text}")
                speaker.say(text)
                speaker.wait()
            else:
                time.sleep(1)


def main():
    rclpy.init()
    node = SubNode("sub_node")
    rclpy.spin(node)
    rclpy.shutdown()