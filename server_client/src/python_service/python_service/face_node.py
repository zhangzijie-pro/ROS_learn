import rclpy
from rclpy.node import Node
from custom_api.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory     # 获得功能包share目录的绝对路径
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.msg import SetParametersResult
import rclpy.parameter

class FaceDetectorNode(Node):
    def __init__(self):
        super().__init__('face_detect')
        self.service = self.create_service(FaceDetector,'face_detect_msg',self.service_callback)
        self.bridge = CvBridge()
        self.declare_parameter('number_of_times_to_upsample',1)
        self.declare_parameter('model',"hog")
        self.number_of_times_to_upsample=self.get_parameter('number_of_times_to_upsample').value
        self.model = self.get_parameter('model').value
        self.image_path = os.path.join(get_package_share_directory('python_service'),'resource/face.jpg')
        self.get_logger().info("Face Detector Server Started!")
        self.add_on_set_parameters_callback(self.parameter_callback)
        # 设置自身节点参数的方法
        self.set_parameters([rclpy.Parameter('model',rclpy.Parameter.Type.STRING,'cnn')])
    
    def parameter_callback(self,paramters):
        for parameter in paramters:
            self.get_logger().info(f"{parameter.name}->{parameter.value}")
            if parameter.name == 'number_of_times_to_upsample':
                self.number_of_times_to_upsample = parameter.value
            if parameter.name == 'model':
                self.model = parameter.value
        return SetParametersResult(successful = True)
    
    def service_callback(self, request, reponse):
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image)
        else:
            cv_image = cv2.imread(self.image_path)
            self.get_logger().info("loading image successfully !... ...")
        start_time = time.time()
        self.get_logger().info("start recogition face ... ...")
        
        face_locations = face_recognition.face_locations(cv_image,self.number_of_times_to_upsample
        ,self.model)
        
        reponse.use_time = time.time()-start_time
        reponse.number = len(face_locations)
        for top,right,bottom,left in face_locations:
            reponse.top.append(top)
            reponse.right.append(right)
            reponse.bottom.append(bottom)
            reponse.left.append(left)
        self.get_logger().info("recogition face Fished!")
        
        return reponse
    
def main():
    rclpy.init()
    node = FaceDetectorNode()
    rclpy.spin(node)
    rclpy.shutdown()