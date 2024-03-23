import rospy
import numpy as np
import math
import cv2
from day4.server_utils_upd import get_target_building
from clover import srv, long_callback
from cv_bridge import CvBridge
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image, Range

c = 0

@long_callback
def image_callback(data):
    global c
    if c % 10 == 0:
        img = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image
        cv2.imwrite(f'cars/car{c}.jpg', img)
        print(f'Saved photo {c}')
    c += 1

image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)
bridge = CvBridge()

rospy.init_node('record')
rospy.spin()