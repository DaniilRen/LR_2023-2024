# подключаем библиотеки для работы с rospy
import rospy
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from cv_bridge import CvBridge, CvBridgeError

# подключаем дополнительные библиотеки
import math
import numpy as np
from datetime import datetime
import cv2


# инициализируем ноду
rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

# фиксируем высоту полета
FLIGHT_HEIGHT = 2

# функция для навигации по полю
def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.6, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

# функция для сохранения фотографии
def save_photo():
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
    now = datetime.now()
    cv2.imwrite(f'{now.strftime("%H-%M-%S")}.jpg', img)
    print('Saved photo')

# главная функция
def main(): 
    # путь для пролета по полю        
    path = [(6, 2), (6, 3), (5, 3), (5, 2), (5.5, 2.5), (6.0, 0.5)]

    navigate_wait(x=0, y=0, z=FLIGHT_HEIGHT, frame_id='body', auto_arm=True)
    print('Takeoff')

    for p in path:
        print(f'flying to x={p[0]}, y={p[1]}, z={FLIGHT_HEIGHT}')
        navigate_wait(x=p[0], y=p[1], z=FLIGHT_HEIGHT, frame_id='aruco_map')
        if p[0] == 5.5 and p[1] == 2.5: # если находимся в середине
            save_photo()
    # посадка
    print('Landing')
    land()


if __name__ == "__main__":
    main()