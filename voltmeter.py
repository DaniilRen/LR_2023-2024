# что-то не то с точностью. 4.6 вместо 4


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

    # возможно не пригодится, так как пока работает аналогично
    # mask = np.zeros(img.shape[:2], dtype='uint8')
    # circle_mask = cv.circle(mask.copy(), (img.shape[1]//2, 370), 325, 255, cv.FILLED)  # маска в виде круга
    # cropped = cv.bitwise_and(img, img, mask=circle_mask)

    cropped = img[195:400, 155:504]
    gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    gray = cv.inRange(gray, 120, 145)
    gray = cv.morphologyEx(gray, cv.MORPH_OPEN, np.ones((3, 3), np.uint8))  # морфол. открытие
    gray = cv.erode(gray, np.ones((3, 3), np.uint8))
    # gray = cv.morphologyEx(gray, cv.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # морфол. открытие

    cv.imshow('res', gray)
    cv.waitKey(0)

    _, contours, __ = cv.findContours(gray, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv.minAreaRect(c)
        area = int(rect[1][0] * rect[1][1])
        if area < 300:
            continue
        box = cv.boxPoints(rect)
        box = np.int64(box)
        ang = round(rect[2])
        cX, cY = map(round, rect[0])
        x, y = box[0]
        # print(cX, cY)
        # print(x, y)

        # new_ang = 180*np.arctan2(x-cX, y-cY)/np.pi
        print(f'-y + cY = {-y + cY}, x - cX = {x - cX}')
        print(f'-y + cY = {-y + cY}, x - cX = {x - cX}')
        new_ang = (np.arctan2(-y + cY, x - cX) * (180 / np.pi)) % 360

        # print(f'rect - {rect}')
        # print(f'box - {box}')
        print(f'counted angle - {ang}')
        print(f'new angle - {new_ang}')
        print()

    print(f'показания вольтметра - {15 * new_ang / 360}')


if __name__ == "__main__":
    img_4 = get_image('https://stepik.org/media/attachments/course/180710/volt_bac2b0686f.png')
    img_10_5 = get_image('https://stepik.org/media/attachments/course/180710/volt_28523493f7.png')
    main(cv.imread('./assets/volt_10_5.png'))
    main(cv.imread('./assets/volt_4_0.png'))