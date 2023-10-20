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


def rotate_img(img_, angle): # собственная, более тонкая реализация
    height, width = img_.shape[:2]
    point = (width//2, height//2)
    mat = cv.getRotationMatrix2D(point, angle, 1) # матрица для поворота
    return cv.warpAffine(img_, mat, (width, height)) # наложение матрицы на картинку

def main(img):
    rotated = rotate_img(img[50:425,100:575], -45)
    gray = cv.cvtColor(rotated, cv.COLOR_BGR2GRAY)
    gray = cv.inRange(gray, 120, 145)
    gray = cv.erode(gray, np.ones((3, 3), np.uint8))
    gray = cv.morphologyEx(gray, np.ones(3, 3))
    _, contours, __ = cv.findContours(gray, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    print(len(contours))
    cv.imshow('img', gray)
    cv.waitKey(0)

if __name__ == "__main__":
    main(get_image('https://stepik.org/media/attachments/course/180710/volt_28523493f7.png'))

# https://stepik.org/media/attachments/course/180710/volt_bac2b0686f.png   - 4.0
# https://stepik.org/media/attachments/course/180710/volt_28523493f7.png   - 10.5