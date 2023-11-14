from urllib.request import urlopen
import numpy as np
import cv2  # v. 3.4.4

COLORS = {
    (0, 0, 255): 'red',
    (0, 255, 0): "green",
    (255, 0, 0): "blue",
    (0, 255, 255): "yellow",
    (0, 165, 255): "orange",
    (0, 0, 0): "black",
    (128, 128, 128): "gray"
}


def get_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def shpe(angles):
    if angles == 3:
        return 'triangle'
    elif angles == 4:
        return 'rectangle'
    elif angles == 5:
        return 'pentagon'
    elif angles == 6:
        return 'hexagon'
    elif angles == 8:
        return 'circle'
    elif angles == 10:
        return 'star'


if __name__ == "__main__":
    img = get_image(input().strip())
    image = img.copy()
    image = cv2.Canny(image, 10, 250)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, np.ones((3, 3)))
    # cv2.imshow('res', image)
    # cv2.waitKey(0)

    _, cont, hier = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shapes = {i: [] for i in range(len(cont))}

    for i in range(len(cont)):
        M = cv2.moments(cont[i])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        shapes[i].append((cx, cy))
        shapes[i].append(COLORS[tuple(img[(cy, cx)])])

    for i in range(len(cont)):
        sm = cv2.arcLength(cont[i], True)
        apd = cv2.approxPolyDP(cont[i], 0.03 * sm, True)
        shapes[i].append(shpe(len(apd)))

    for k in shapes:
        print(shapes[k][2], shapes[k][1], *shapes[k][0])