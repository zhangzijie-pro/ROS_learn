import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory     # 获得功能包share目录的绝对路径

def main():
    face_image_path = get_package_share_directory('python_service')+'/resource/face.jpg'
    print(f"file path: {face_image_path}")
    img = cv2.imread(face_image_path)
    face_location = face_recognition.face_locations(img,number_of_times_to_upsample=1
    ,model="hog")
    for top,right,bottom,left in face_location:
        cv2.rectangle(img,(left,top),(right,bottom),(255,0,0),4)
        
    cv2.imshow("result",img)
    cv2.waitKey(0)