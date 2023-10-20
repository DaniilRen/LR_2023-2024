from urllib.request import urlopen
import cv2 as cv # v. 3.4.18.65
import numpy as np
import math


def get_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image


def round_(num, step): # округляет с шагом 0.5
    return round(num / step) * step

def main(img):
    cropped = img[195:405, 165:495]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    gray = cv.inRange(gray, 120, 145)
    gray = cv.erode(gray, np.ones((3, 3), np.uint8))
    _, contours, __ = cv.findContours(gray, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    rect = cv.minAreaRect(contours[0])
    box = cv.boxPoints(rect)
    box = np.int64(box)
    min_ang = round(rect[2])
    print(min_ang)
    M = cv.moments(contours[0])
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    x, y = box[0]

    # angle = (np.arctan2(-y + cY, x - cX) * (180 / np.pi)) % 360

    startpoint = (img.shape[1] // 2, 0)
    endpoint = box[0]
    print(box)
    print(startpoint, endpoint)
    # angle = math.degrees(math.atan2(rect[1][1]-y, rect[1][0]-x))
    angle = math.degrees(math.atan2(startpoint[1] - endpoint[1], startpoint[0] - endpoint[0]))
    # angle = math.degrees(math.atan2(startpoint[0] - endpoint[0], startpoint[1] - endpoint[1]))
    # если нужен диапазон 0..360
    # if new_angle < 0:
    #     angle += 180

    print((15 * angle / 360))
    print('result', round_((15 * angle / 360), 0.5))
    print(len(contours))
    cv.rectangle(gray, (x, y), (cX, cY), 71, 1)
    cv.rectangle(gray, startpoint, endpoint, 123, 1)
    cv.rectangle(gray, (185, 208), (188, 209), 76, 3)
    cv.imshow('res', gray)
    cv.waitKey(0)

def main_(img):
    cropped = img[195:405, 165:495]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    gray = cv.inRange(gray, 120, 145)
    gray = cv.erode(gray, np.ones((3, 3), np.uint8))
    _, contours, __ = cv.findContours(gray, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    end = [0, 0]
    start = [1000, 1000]
    for p in contours[0]:
        p = p[0]
        if p[0] < start[0]:
            start = p
        if p[0] > end[0]:
            end = p

    angle_ = math.degrees(math.atan2(start[1] - end[1], start[0] - end[0]))
    angle = (np.arctan2(start[1] - end[1], start[0] - start[0]) * (180 / np.pi)) % 360
    # if angle < 0:
    #     angle += 360

    print(start, end)
    print(angle)
    print(angle_)
    print(end[0]-start[0]*15/360)
    print(end[0]-start[0]*15/270)
    print(end[0]-start[0]*15/180)
    print(end[0]-start[0]*15/90)
    print((15 * angle / 360))
    cv.rectangle(gray, start, end, 176, 1)
    cv.imshow('res', gray)
    cv.waitKey(0)

if __name__ == "__main__":
    main_(get_image('https://stepik.org/media/attachments/course/180710/volt_28523493f7.png'))

# https://stepik.org/media/attachments/course/180710/volt_bac2b0686f.png   - 4.0
# https://stepik.org/media/attachments/course/180710/volt_28523493f7.png   - 10.5