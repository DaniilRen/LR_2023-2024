import rospy
import math
from clover import srv
from mavros_msgs.srv import CommandBool 
from std_srvs.srv import Trigger 
from std_msgs.msg import Float64

rospy.init_node('flight')

navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global =rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
get_telemetry =rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


navigate_wait(z=1, frame_id='body', auto_arm=True)
print('1')

navigate_wait(x=3, y=2, z=1, frame_id='aruco_map')
print('2')
land()