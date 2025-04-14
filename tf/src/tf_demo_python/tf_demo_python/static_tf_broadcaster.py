import rclpy
from rclpy.node import Node
import math
from tf2_ros import StaticTransformBroadcaster  # 静态坐标发布器
from geometry_msgs.msg import TransformStamped  # 消息接口
from tf_transformations import quaternion_from_euler    # 欧拉角变化公式

class StaticTFBroadcaster(Node):
    def __init__(self):
        super().__init__("static_tf_broadcaster")
        self.tf_broadcaster_ = StaticTransformBroadcaster(self)
        self.publish_static_tf()
    
    def publish_static_tf(self):
        transform = TransformStamped()
        transform.header.frame_id = "base_link"
        transform.header.stamp=self.get_clock().now().to_msg()
        transform.child_frame_id='camera_link'
        
        transform.transform.translation.x = 0.5
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.6
        
        # euler return (x,y,z,w)
        q=quaternion_from_euler(math.radians(180),0,0)
        transform.transform.rotation.x=q[0]
        transform.transform.rotation.y=q[1]
        transform.transform.rotation.z=q[2]
        transform.transform.rotation.w=q[3]
        
        self.tf_broadcaster_.sendTransform(transform)
        self.get_logger().info(f"publish static tf: --> {transform}\n -------")
    
    
def main():
    rclpy.init()
    node = StaticTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()