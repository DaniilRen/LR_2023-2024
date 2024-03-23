# подключаем библиотеки для работы с rospy
import rospy
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image, Range
from cv_bridge import CvBridge
from cv_bridge import CvBridge

# подключаем дополнительные библиотеки
from utils import *
import math
import numpy as np
from datetime import datetime
import cv2

# функции получения информации с сервисов
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)


class Copter():
    def __init__(self, stream) -> None:
        self.stream = stream

    # установка значений для полета
    def set_params(self, speed, flight_height, frame_id='aruco_map'):
        self.flight_height = flight_height
        self.stream.set_flight_height(flight_height)
        self.speed = speed
        self.frame_id = frame_id

    # функция генерации маршрута
    def set_route(self, func):
        self.route = func()

    # запись координат начальной позиции
    def set_start_point(self):
        telem = get_telemetry(frame_id='aruco_map')
        self.start_point = (telem.x, telem.y)
        print(f'start point set in x={telem.x}, y={telem.y}')

    # функция взлета
    def takeoff(self):
        print('takeoff')
        self.navigate_wait(z=1.75, frame_id='body', auto_arm=True)
        print('waiting for next action')
    
    # функция посадки
    def land_wait(self):
        land()
        while get_telemetry().armed:
            rospy.sleep(0.2)

    # функция для навигации по полю
    def navigate_wait(self, x=0, y=0, z=None, yaw=float('nan'),
                        speed=None, frame_id=None,
                        auto_arm=False, tolerance=0.2):
        if speed == None:
            speed = self.speed
        if frame_id == None:
            frame_id = self.frame_id
        if z == None:
            z = self.flight_height

        print(f'flying to x={x}, y={y}, z={z}')
        navigate(x=x, y=y, z=z, yaw=yaw, speed=speed,
                    frame_id=frame_id, auto_arm=auto_arm)

        while not rospy.is_shutdown():
            telem = get_telemetry(frame_id='navigate_target')
            if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
                break
            rospy.sleep(0.2)

    # полет к зданию особого итереса
    def navigate_target_building(self):
        print('navigating to special building')
        # берем координаты с сервера
        coords = get_server_coords(self.stream.buildings_data)
        if coords != None:
            self.navigate_wait(x=coords[0], y=coords[1], z=self.flight_height)
            rospy.sleep(0.3)
            # высота здания
            height = get_building_height(self.flight_height)
            print(f'building height: {height}')
            print(f'flying to x={coords[0]}, y={coords[1]}, z={height+0.5}')
            self.navigate_wait(x=coords[0], y=coords[1], z=height+0.5)
            # сохраняем фото
            rospy.sleep(0.3)
            self.stream.save_photo()
            rospy.sleep(0.3)
            print(f'flying to x={coords[0]}, y={coords[1]}, z={self.flight_height}')
            self.navigate_wait(x=coords[0], y=coords[1], z=self.flight_height)
            rospy.sleep(0.3)
            return 0
        print('Error while connecting to server')
        return 1    


class Stream():
    def __init__(self, main_topic='main_camera/image_raw') -> None:
        self.main_topic = main_topic
        self.bridge = CvBridge()
        self.main_sub = rospy.Subscriber(main_topic, Image, self.main_callback)
        self.buildings_data = {}
        self.not_detected_colors = ['green', 'red', 'blue', 'yellow']

    # функция для сохранения фотографии
    def save_photo(self):
        img = self.bridge.imgmsg_to_cv2(rospy.wait_for_message(self.main_topic, Image), 'bgr8')
        now = datetime.now()
        name = f'{now.strftime("%H-%M-%S")}.jpg'
        cv2.imwrite(name, img)
        print(f'Saved photo {name}')

    # callback для видеопотока
    def main_callback(self, data):
        img = self.bridge.imgmsg_to_cv2(data, 'bgr8')

        if self.not_detected_colors:
            new = self.detect_building(img)
            if new:
                self.buildings_data[new[0]] = new[1:]

    # установка высоты полета для распознавания зданий
    def set_flight_height(self, flight_height):
        self.flight_height = flight_height
    
    # метод проверки позиции найденого здания
    def check_building_pos(self, center, size=(320, 240)):
        xc, yc = size[0] / 2, size[1] / 2
        x1, y1, x2, y2 = xc - 32, yc - 12, xc + 32, yc + 12
        if center[0] <= x1 or center[0] >= x2 or center[1] <= y1 or center[1] >= y2:
            return False
        return True
    
    # метод определений этажности здания
    def get_floors_info(self, floors):
        height = get_building_height(self.flight_height)
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
    def detect_building(self, frame):
        # переводим кадр в hsv формат
        frame = to_hsv(frame)
        thresholds = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
                'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
                'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
                'yellow': {'Lower': np.array([21, 88, 149]), 'Upper': np.array([35, 215, 255])},
                }
        floors = {'red': 4,
                    'blue': 3,
                    'green': 2,
                    'yellow': 1}
        
        for color in self.not_detected_colors:
            inRange_hsv = cv2.inRange(frame, thresholds[color]['Lower'], thresholds[color]['Upper'])
            cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            frame_vol = np.prod(frame.shape[0:2])
            if cnts:
                fraction = 0.005
                # Фильтруем объекты по площади
                assert frame_vol != 0
                cnts = list(filter(lambda c: (cv2.contourArea(c) / frame_vol) >= fraction and (cv2.contourArea(c) / frame_vol) < 0.2, cnts))

                if cnts:
                    # ищем контур с наибольшей площадью
                    c = max(cnts, key=cv2.contourArea)
                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                            
                    x = box[0][0]
                    y = box[0][1]
                    height = box[2][1] - y
                    width = box[1][0] - x
                    # центр найденного контура
                    center = [x + width / 2, y + height / 2]
                    if self.check_building_pos(center):
                        # убираем из поиска здание найденного цвета
                        self.not_detected_colors.remove(color)
                        expected_floors = floors[color]
                        real_floors, flag_reality = self.get_floors_info(expected_floors)
                        t = get_telemetry(frame_id='aruco_map')
                        coords = round_coords([t.x, t.y])
                        print(f'{color} building found, x={coords[0]}, y={coords[1]}')
                        return [color, coords, real_floors, expected_floors, flag_reality]