from urllib.request import urlopen
import cv2 as cv # v. 3.4.4
import numpy as np


def get_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image

def main():
    # img = get_image('https://stepik.org/media/attachments/course/122772/clock_88e05d50-3c38-49e4-977f-8b2bf8c62b64.jpg')
    img = cv.imread('./assets/clock.jpg')
    cropped = img[200:400, 200:400]  # обрезаем изображение до квадрта посередине
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    black = cv.inRange(gray, 0, 19)  # для черной стрелки
    red = cv.inRange(cropped, (0, 0, 220), (30, 30, 255))

    _, con, __ = cv.findContours(black, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in con:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        min_ang = round(rect[2])
        print(min_ang)
        cv.drawContours(black, [box], 0, (0, 0, 255), 2)

    _, con, __ = cv.findContours(red, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in con:
        if cv.contourArea(cnt) > 60:
            rect = cv.minAreaRect(cnt)
            area = int(rect[1][0] * rect[1][1])
            if area < 60:
                continue
            h_ang = round(rect[2])
            print(h_ang)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            cv.drawContours(red, [box], 0, (0, 0, 255), 3)

    hrs = 12 * h_ang / 360
    mins = 60 * min_ang / 360

    print(f"{round(hrs)} : {round(mins)}")
    cv.imshow('', red)  # смотрел картинку
    cv.waitKey(0)

if __name__ == "__main__":
    main()