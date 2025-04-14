import rclpy
from rclpy.node import Node
import math
from tf2_ros import TransformBroadcaster  # 动态坐标发布器
from geometry_msgs.msg import TransformStamped  # 消息接口
from tf_transformations import quaternion_from_euler    # 欧拉角变化公式

class DynamicFBroadcaster(Node):
    def __init__(self):
        super().__init__("dynamic_tf_broadcaster")
        self.tf_broadcaster_ = TransformBroadcaster(self)
        self.timer = self.create_timer(0.01,self.publish_tf)
    
    def publish_tf(self):
        transform = TransformStamped()
        transform.header.frame_id = "camera_link"
        transform.header.stamp=self.get_clock().now().to_msg()
        transform.child_frame_id='bottle_link'
        
        transform.transform.translation.x = 0.2
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5
    
        # euler return (x,y,z,w)
        q=quaternion_from_euler(0,0,0)
        transform.transform.rotation.x=q[0]
        transform.transform.rotation.y=q[1]
        transform.transform.rotation.z=q[2]
        transform.transform.rotation.w=q[3]
        
        self.tf_broadcaster_.sendTransform(transform)
        self.get_logger().info(f"publish tf: --> {transform}\n -------")
    
    
def main():
    rclpy.init()
    node = DynamicFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()