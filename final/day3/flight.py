# подключаем библиотеки для работы с rospy
import rospy
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image, Range
from cv_bridge import CvBridge
from cv_bridge import CvBridge, CvBridgeError

# подключаем дополнительные библиотеки
from server_utils import *
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
# координаты центра зоны
MIDDLE_POINT = [5.5, 2.5]

size = 240, 320 # размер для обрезки изображения при детекции зданий
clover_path = []
data_build = {}
bridge = CvBridge()
colors = ['green', 'red', 'blue', 'yellow'] # цвета зданий
# используется для учета пройденных зданий
colors_detect  = ['green', 'red', 'blue', 'yellow']
target_building_coords = []

floors = {'red': 4,
                  'blue': 3,
                  'green': 2,
                  'yellow': 1}

colors_path = {'red': [6, 2],
               'blue': [6, 4],
               'green': [5, 4],
               'yellow': [5, 2]}

# Пороговые значения HSV для детектиования зданий
thresholds = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'yellow': {'Lower': np.array([21, 88, 149]), 'Upper': np.array([35, 215, 255])},
              }

# обработка изображений с камеры
def image_callback(data):
    global colors_detect
    global data_build
    img = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image

    if colors_detect:
        array = detect_building(img, colors_detect)
        if array:
            print(array)
            colors_detect = array[0]
            # data_build.append((array[0], array[1:]))
            data_build[array[1]] = array[2:]
            print(data_build)


# функция для навигации по полю
def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
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


# метод генерации маршрута полёта
def rout_generation():
    result = []
    for i in range(0, 7, 1):
        for j in range(0, 7, 1):
            if i % 2 == 0:
                result.append([7 - (j / 2), 1 + (i / 2)])
            else:
                result.append([4 + (j / 2), 1 + (i / 2)])
    result.append([5.5, 2.5])
    return result


# метод преоброзования изображения в формат HSV
def hsv_frame(frame):
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0) #  Размытие по Гауссу
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV) #  Преобразовать в изображение HSV
    erode_hsv = cv2.erode(hsv, None, iterations=2) #  Коррозия Грубое разбавление
    return erode_hsv


# метод проверки позиции найденого здания
def check_building_pos(coords):
    size = [320, 240]
    xc, yc = size[0] / 2, size[1] / 2
    x1, y1, x2, y2 = xc - 32, yc - 12, xc + 32, yc + 12
    if coords[0] <= x1 or coords[0] >= x2 or coords[1] <= y1 or coords[1] >= y2:
        return False
    return True


# метод определений этажности здания
def get_floors_info(floors):
    dist = rospy.wait_for_message('rangefinder/range', Range).range
    height = FLIGHT_HEIGHT - dist
    if height >= 0.95:
        count = 4
    elif 0.7 <= height < 0.95:
        count = 3
    elif 0.45 <= height < 0.7:
        count = 2
    else:
        count = 1
    if floors == count:
        return count, True
    return count, False


# метод нахождения зданий
def detect_building(frame, colors):
    frame = hsv_frame(frame)
    for color in colors:
        inRange_hsv = cv2.inRange(frame, thresholds[color]['Lower'], thresholds[color]['Upper'])
        cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        frame_vol = np.prod(frame.shape[0:2])
        if cnts:
            # print(cnts)
            fire_fraction = 0.005
            # Фильтруем объекты по площади
            assert frame_vol != 0
            cnts = list(filter(lambda c: (cv2.contourArea(c) / frame_vol) >= fire_fraction and (cv2.contourArea(c) / frame_vol) < 0.2, cnts))

            if cnts:
                c = max(cnts, key=cv2.contourArea)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                        
                x = box[0][0]
                y = box[0][1]
                height = box[2][1] - y
                width = box[1][0] - x
                center = [x + width / 2, y + height / 2]
                if check_building_pos(center):
                    colors.remove(color)
                    expected_floors = floors[color]
                    real_floors, flag_reality = get_floors_info(expected_floors)
                    t = get_telemetry(frame_id='aruco_map')
                    return [colors,  color, [t.x, t.y], real_floors, expected_floors, flag_reality]


# полет к зданию особого итереса
def navigate_target_building():
    print('navigating to target building')
    global data_build
    coords = get_target_building(data_build)
    navigate_wait(x=coords[0], y=coords[1], z=FLIGHT_HEIGHT)
    rospy.sleep(0.3)
    dist = rospy.wait_for_message('rangefinder/range', Range).range
    height = FLIGHT_HEIGHT - dist
    navigate_wait(x=coords[0], y=coords[1], z=height+0.5)
    rospy.sleep(0.3)
    save_photo()
    rospy.sleep(0.3)
    navigate_wait(x=coords[0], y=coords[1], z=FLIGHT_HEIGHT)


# главная функция
def main():
    image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)
    # путь для пролета по полю
    path = rout_generation()
    path.append([6.0, 0,5])

    navigate_wait(x=0, y=0, z=FLIGHT_HEIGHT, frame_id='body', auto_arm=True)
    print('Takeoff')

    for p in path:
        print(f'flying to x={p[0]}, y={p[1]}, z={FLIGHT_HEIGHT}')
        navigate_wait(x=p[0], y=p[1], z=FLIGHT_HEIGHT, frame_id='aruco_map')
        if p == MIDDLE_POINT: # если находимся в середине
            save_photo()
        if len(path) == 1:
            navigate_target_building()
        path.pop(0)
    # посадка
    print('Landing')
    land()


if __name__ == "__main__":
    main()