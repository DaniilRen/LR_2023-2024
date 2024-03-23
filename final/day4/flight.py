# подключаем библиоте99ки для работы с rospy
import rospy
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image, Range
from cv_bridge import CvBridge
from cv_bridge import CvBridge

# подключаем дополнительные библиотеки
from server_utils import *
import math
import numpy as np
from datetime import datetime
import cv2


# инициализируем ноду
rospy.init_node('flight')
# функции получения информации с сервисов
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

bridge = CvBridge()

# высота полета
FLIGHT_HEIGHT = 1.7

# координаты центра зоны
START_POINT = [6.5, 0.4]

# координаты начальной точки
MIDDLE_POINT = [5.5, 2.5]

# данные для отправки на сервер
data_build = {}

# цвета зданий
colors = ['green', 'red', 'blue', 'yellow']

# используется для учета пройденных зданий
colors_detect  = ['green', 'red', 'blue', 'yellow']

# этажность в зависимости от цвета здания
floors = {'red': 4,
                  'blue': 3,
                  'green': 2,
                  'yellow': 1}

# thresholds = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
#              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
#             'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
#             'yellow': {'Lower': np.array([21, 88, 149]), 'Upper': np.array([35, 215, 255])},
#              }
# Пороговые значения HSV для детектиования зданий
thresholds = {'red': {'Lower': np.array([0, 156, 193]), 'Upper': np.array([196, 200, 255])},
              'blue': {'Lower': np.array([183, 0, 0]), 'Upper': np.array([255, 201, 137])},
              'green': {'Lower': np.array([89, 190, 0]), 'Upper': np.array([151, 255, 138])},
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
            colors_detect = array[0]
            data_build[array[1]] = array[2:]


# функция для навигации по полю
def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.3, frame_id='', auto_arm=False, tolerance=0.2):
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
    # получение данных с дальномера
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


# округление координат с шагом 0.5
def round_coords(coords):
  return [round(coords[0] * 2) / 2, round(coords[1] * 2) / 2]


# метод нахождения зданий
def detect_building(frame, colors):
    # переводим кадр в hsv формат
    frame = hsv_frame(frame)
    for color in colors:
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
                if check_building_pos(center):
                    # убираем из поиска здание найденного цвета
                    colors.remove(color)
                    expected_floors = floors[color]
                    real_floors, flag_reality = get_floors_info(expected_floors)
                    t = get_telemetry(frame_id='aruco_map')
                    coords = round_coords([t.x, t.y])
                    print(f'{color} building found, x={coords[0]}, y={coords[1]}')
                    return [colors,  color, coords, real_floors, expected_floors, flag_reality]


# полет к зданию особого итереса
def navigate_target_building():
    print('navigating to special building')
    global data_build
    # берем координаты с сервера
    coords = get_target_building(data_build)
    if coords != None:
        navigate_wait(x=coords[0], y=coords[1], z=FLIGHT_HEIGHT)
        rospy.sleep(0.3)
        # получение данных с дальномера
        dist = rospy.wait_for_message('rangefinder/range', Range).range
        # высота здания
        height = FLIGHT_HEIGHT - dist
        print(f'building height: {height}')
        print(f'flying to x={coords[0]}, y={coords[1]}, z={height+0.5}')
        navigate_wait(x=coords[0], y=coords[1], z=height+0.5)
        # сохраняем фото
        rospy.sleep(0.3)
        save_photo()
        rospy.sleep(0.3)
        print(f'flying to x={coords[0]}, y={coords[1]}, z={FLIGHT_HEIGHT}')
        navigate_wait(x=coords[0], y=coords[1], z=FLIGHT_HEIGHT)
        rospy.sleep(0.3)
        return 0
    print('Error while connecting to server')
    return 1    


# главная функция полета
def main():
    # подписчик на топик с изображениями с камеры
    image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)
    # путь для пролета по полю
    path = rout_generation()

    print('Takeoff')
    navigate_wait(x=0, y=0, z=FLIGHT_HEIGHT, frame_id='body', auto_arm=True)
    rospy.sleep(0.5)
    print('Starting path flying')

    for p in path:
        print(f'flying to x={p[0]}, y={p[1]}, z={FLIGHT_HEIGHT}')
        navigate_wait(x=p[0], y=p[1], z=FLIGHT_HEIGHT, frame_id='aruco_map')
        if p == MIDDLE_POINT: # если находимся в середине
            print('Middle point found')
            # сохраняем фото
            rospy.sleep(0.3)
            save_photo()
            rospy.sleep(0.3)
    # отправка данных и полет к зданию особого интереса
    navigate_target_building()
    # возвращение на стартовую платформу и посадка
    navigate_wait(x=START_POINT[0], y=START_POINT[1], z=FLIGHT_HEIGHT, frame_id='aruco_map')
    print('Landing')
    land()


if __name__ == "__main__":
    main()
