import rclpy
from rclpy.node import Node
import rclpy.time
from tf2_ros import TransformListener,Buffer  # 坐标变换监听器
from tf_transformations import euler_from_quaternion    # 欧拉角变化公式

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__("tf_broadcaster")
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer,self)
        self.timer = self.create_timer(1.0,self.get_transform)
    
    def get_transform(self):
        try:
            result = self.buffer.lookup_transform('base_link','bottle_link'
                ,rclpy.time.Time(seconds=0.0),rclpy.time.Duration(seconds=1.0))
            transform = result.transform
            self.get_logger().info(f"平移:{transform.translation}")
            self.get_logger().info(f"旋转:{transform.rotation}") 
            rotation_euler = euler_from_quaternion(
                [transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w]
                )
            self.get_logger().info(f"旋转:{rotation_euler}")   
              
        except Exception as e:
            self.get_logger().error(f"{e}")
    
def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()