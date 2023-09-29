from urllib.request import urlopen
import cv2 as cv # v. 3.4.18.65
import numpy as np


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

    _, contours, __ = cv.findContours(gray, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv.contourArea(c) < 100:
            continue

        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int64(box)
        M = cv.moments(c)
        cX = int(M['m10'] / M['m00']) # координаты центра
        cY = int(M['m01'] / M['m00'])
        x, y = box[0] # координаты конца стрелки

        if x < gray.shape[1]/2: # если стрелка в левой части картинки
            cX -= 20 # имперически подобрал

        ang = (np.arctan2(-y + cY, x - cX) * (180 / np.pi)) % 360
        break

    print(round_((15 * ang / 360), 0.5))
    print(15 * ang / 360)


if __name__ == "__main__":
    main(get_image(input()))