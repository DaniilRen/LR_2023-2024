import numpy as np
import cv2
import math


imageFrame1 = cv2.imread('./assets/volt_4_0.png')
(w, h, c) = imageFrame1.shape
imageFrame = cv2.resize(imageFrame1, (700, 500))
# imageFrame=cv2.rotate(imageFrame2,cv2.ROTATE_90_CLOCKWISE)
hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

lower = np.array([61, 0, 193], np.uint8)
upper = np.array([255, 255, 255], np.uint8)
mask = cv2.inRange(hsvFrame, lower, upper)
cv2.imshow('1 - HSV', hsvFrame)

kernal = np.ones((5, 5), "uint8")

mask = cv2.dilate(mask, kernal)
res = cv2.bitwise_and(imageFrame, imageFrame, mask=mask)
cv2.imshow('2 - Mask', mask)

# поиск контура вольтметра
_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if (area > 20000 and area < 60000):
        x, y, w, h = cv2.boundingRect(contour)
# print(x, y) #203 124
# print(w,h)  #270 188
# imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (255, 0, 0), 1)
# cv2.putText(imageFrame, "VOLTMETER", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))
current = imageFrame[124 + 20:124 + 188 - 7, 203 + 5:203 + 270 - 5]
# current = imageFrame[ + 20:y + h - 7, x + 5:x + w - 5]
# cv2.imwrite("volt_current.jpg", current)
cv2.imshow("3 - Only Voltmeter", current)

# создание окна эллипса
imageEllipse = np.zeros((188 - 27, 270 - 10, 3), np.uint8)
imageEllipse[:] = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
height, width = imageEllipse.shape[0:2]

# дуга 205-270 градусов (чтобы не налазила на шкалу)
radius1_1 = 95
radius1_2 = 90
center1 = (int(width / 2), int(height / 2 + 27) + 80)
axes1 = (radius1_1, radius1_2)
angle1 = 0
startAngle1 = 205
endAngle1 = 270
thickness1 = 2

# дуга 270-340 градусов
radius2_1 = 85
radius2_2 = 90
center2 = (int(width / 2), int(height / 2 + 27) + 80)
axes2 = (radius2_1, radius2_2)
angle2 = 0
startAngle2 = 270
endAngle2 = 340
thickness2 = 2  # When thickness == -1 -> Fill shape

cv2.ellipse(imageEllipse, center1, axes1, angle1, startAngle1, endAngle1, BLACK, thickness1)
cv2.ellipse(imageEllipse, center2, axes2, angle2, startAngle2, endAngle2, BLACK, thickness2)

imageEllipse1 = cv2.cvtColor(imageEllipse, cv2.COLOR_BGR2GRAY)

imageEllipse2 = cv2.threshold(imageEllipse1, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imshow('4 - ellipse mask', imageEllipse2)
cv2.imshow('ellipse1', imageEllipse1)

mask = np.array(imageEllipse2)
mask1 = np.array(imageEllipse1)
img = current.copy()
img = cv2.GaussianBlur(img, (3, 3), 0)
edge = cv2.Canny(img, 35, 15)
cv2.imshow('5 - Canny', edge)
res1 = cv2.bitwise_and(current, current, mask=mask1)

res = cv2.bitwise_and(edge, edge, mask=mask)
cv2.imshow('7 - Res', res)

_, contours, hierarchy = cv2.findContours(res.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    if (h >= 2 and w > 2):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        theta = 180 / math.pi * math.atan((y - (height / 2 + 27 + 120)) / (x - (int(width / 2))))
        theta0 = 45
        if theta < theta0:
            volt = 0
        if volt < 0:
            volt = 0
        volt_prev = volt
        volt = (theta - theta0) / 0.4
        delta = volt - volt_prev
        if delta <= 2 and volt > 0:
            tec_volt = int(volt)
            print(tec_volt)

cv2.imshow('6 - Voltmeter+ellipse', res1)
cv2.waitKey(0)