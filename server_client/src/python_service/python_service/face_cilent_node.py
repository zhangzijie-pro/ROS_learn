import rclpy
from rclpy.node import Node
from custom_api.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory     # 获得功能包share目录的绝对路径
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,ParameterValue, ParameterType

class FaceDetectorClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.bridge = CvBridge()
        self.image_path = os.path.join(get_package_share_directory('python_service'),
        'resource/test.jpg')
        self.client = self.create_client(FaceDetector,"face_detect_msg")
        self.cv2_img = cv2.imread(self.image_path)
        self.get_logger().info("Face Detector Client Started!")
    
    def call_set_parameters(self,parameters):
        '''
        调用服务，修改参数值
        '''
        update = self.create_client(SetParameters,"/face_detect/set_parameters")
        while self.client.wait_for_service(1.0) is False:
            self.get_logger().info("Waiting for server up!")
        request = SetParameters.Request()
        request.parameters = parameters
        future = update.call_async(request)
        rclpy.spin_until_future_complete(self,future)
        response = future.result()
        return response
    
    def update_detect_model(self,model="hog"):
        param = Parameter()
        param.name = 'model'
        P_value = ParameterValue()
        P_value.string_value=model
        P_value.type = ParameterType.PARAMETER_STRING
        param.value = P_value
        response = self.call_set_parameters([param])
        for result in response.results:
            self.get_logger().info(f"parameter result: {result.successful} {result.reason}")
        
    
    def send_request(self):
        while self.client.wait_for_service(1.0) is False:
            self.get_logger().info("Waiting for server up!")
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.cv2_img)
        future = self.client.call_async(request=request) # 现在的future并没有包含响应结果，需要等待服务
        #while not future.done():
        #   time.sleep(1.0)
        # rclpy.spin_until_future_complete(self,future)
        def call_back_result(result_future):
            response = result_future.result()
            self.get_logger().info(f"get message, there are {response.number}'s face, spend time {response.use_time} s")
            #self.show_reponse(response)
            
        future.add_done_callback(call_back_result)
    
    def show_reponse(self, response):
        for i in range(response.number): 
            top = response.top[i]
            left = response.left[i]
            bottom = response.bottom[i]
            right = response.right[i]
            cv2.rectangle(self.cv2_img,(left,top),(right,bottom),(255,0,0),4)
        cv2.imshow("result",self.cv2_img)
        cv2.waitKey(0)
        
def main():
    rclpy.init()
    node = FaceDetectorClientNode()
    node.update_detect_model('hog')
    node.send_request()
    node.update_detect_model('cnn')
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()