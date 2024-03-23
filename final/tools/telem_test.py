import rospy
import numpy as np
import math
import cv2
from day4.server_utils_upd import get_target_building
from clover import srv, long_callback
from cv_bridge import CvBridge
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image, Range

from datetime import datetime
from day4.server_utils_upd import *


get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)


while not rospy.is_shutdown():
    print(get_telemetry.data)