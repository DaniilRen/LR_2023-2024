import cv2 as cv
import numpy as np


def main():
    img = np.zeros((100, 100), np.uint8)

    for i in range (int(input())):
        shape = input().split()
        if shape[0] == 'rectangle':
            ulx, uly, drx, dry, color, thic = map(int, shape[1:])
            cv.rectangle(img, (ulx, uly), (drx, dry), color, thic)
        elif shape[0] == 'circle':
            cx, cy, r, color, thic = map(int, shape[1:])
            cv.circle(img, cx, cy, r, color, thic)
        elif shape[0] == 'point':
            x, y, color = map(int, shape[1:])
            img[y, x] = color

    np.set_printoptions(threshold=np.inf)
    for i in img:
        print(*i)


if __name__ == "__main__":
    main()