from urllib.request import urlopen
import cv2 as cv # v. 3.4.18.65
import numpy as np
import math


def get_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image


def round_(num, step):  # округляет с шагом 0.5
    return round(num / step) * step


def coords_max_pixel(img):
    x, y = img.shape
    for i in range(x):
        for j in range(y):
            if img[i, j] == 255:
                return i, j


def coords_min_pixel(img):
    x, y = img.shape
    for j in range(y):
        if img[x - 1, j] == 255:
            return x - 1, j


def tg_rad(a, b):
    x = abs(a[0] - b[0])
    y = b[1] - a[1]
    if y > 0:
        tg = x / y
        return tg, False
    tg = x / abs(y)
    return tg, True


def cretnost(doltan):
    while doltan % 0.5 != 0:
        doltan += 0.1
    return doltan


def main(img):
    cropped = img[185:403, 115:565]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    gray = cv.inRange(gray, 120, 145)
    gray = cv.erode(gray, np.ones((3, 3), np.uint8))
    coords_a = coords_max_pixel(gray)
    coords_b = coords_min_pixel(gray)

    tg_ang, flag = tg_rad(coords_a, coords_b)
    ang = math.atan(tg_ang) * 180 / math.pi - 46.5
    if flag:
        result = 15 - cretnost(round(ang * 15 / 90, 1))
    else:
        result = cretnost(round(ang * 15 / 90, 1))
    return result


if __name__ == "__main__":
    print(main(get_image(input())))
