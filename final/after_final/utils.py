import cv2
import rospy
from sensor_msgs.msg import Range

# округление координат с шагом 0.5
def round_coords(coords):
  return [round(coords[0] * 2) / 2, round(coords[1] * 2) / 2]

# метод преоброзования изображения в формат HSV
def to_hsv(frame):
    blurred = cv2.GaussianBlur(frame, (5, 5), 0) #  размытие по Гауссу
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) #  преобразание в HSV формат
    eroded = cv2.erode(hsv, None, iterations=2) #  коррозия
    return eroded

# метод определений высоты здания
def get_building_height(flight_height):
    # получение данных с дальномера
    dist = rospy.wait_for_message('rangefinder/range', Range).range
    height = flight_height - dist
    return height

# КОД-ЗАГЛУШКА, так как сервер нерабочий
# получение данных с сервера
def get_server_coords(data):
    # менять эти значения по необходимости
    response = [6.5, 2.5]
    status_code = 200

    if status_code == 200:
        print(f"JSON Response {status_code}")
        return response
    return None