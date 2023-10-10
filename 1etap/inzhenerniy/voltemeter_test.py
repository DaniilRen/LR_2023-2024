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
        rect = cv.minAreaRect(c)
        area = int(rect[1][0] * rect[1][1])
        if area < 60:
            continue


        box = cv.boxPoints(rect)
        box = np.int64(box)
        min_ang = round(rect[2])
        print(min_ang)
        M = cv.moments(c)
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        x, y = box[0]
        # cX = rect[1][0]
        # cY = rect[1][1]
        # x = rect[0][0]
        # y = rect[0][1]

        if x < gray.shape[1]/2: # если стрелка в левой части картинки
            cX -= 20 # имперически подобрал

        # ang = 180*np.arctan2(x-cX, y-cY)/np.pi
        ang = (np.arctan2(-y + cY, x - cX) * (180 / np.pi)) % 360

        print(f'Moments cx cy: {cX}, {cY}')
        print(f'x: {x}, y: {y}')
        print(f'-y + cY = {-y + cY}, x - cX = {x - cX}')
        print(f'-y + cY = {-y + cY}, x - cX = {x - cX}')
        print(f'rect - {rect}')
        print(f'box - {box}')
        print(f'counted angle - {ang}')
        break

    print(f'x: {x}, width/2: {gray.shape[1]/2}')
    print((15 * ang / 360))
    print('result', round_((15 * ang / 360), 0.5))
    cv.rectangle(gray, (x, y), (cX, cY), 71, 2)
    cv.imshow('res', gray)
    cv.waitKey(0)



if __name__ == "__main__":
    main(get_image('https://stepik.org/media/attachments/course/180710/volt_bac2b0686f.png'))