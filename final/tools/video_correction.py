import cv2 as cv
import numpy as np

def nothing(x):
    pass


def main(type='video', src=0, format='bgr', edit=False, size=0):
    cv.namedWindow('result')
    cv.createTrackbar('min 1', 'result', 0, 255, nothing)
    cv.createTrackbar('min 2', 'result', 0, 255, nothing)
    cv.createTrackbar('min 3', 'result', 0, 255, nothing)
    cv.createTrackbar('max 1', 'result', 0, 255, nothing)
    cv.createTrackbar('max 2', 'result', 0, 255, nothing)
    cv.createTrackbar('max 3', 'result', 0, 255, nothing)

    if type == 'video':
        cap = cv.VideoCapture(src)
    while True:
        if type == 'video':
            ret, frame = cap.read()
            if format == 'hsv':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            elif format == 'lab':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            elif format == 'rgb':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        elif type == 'image':
            frame = cv.imread(src)
            if format == 'hsv':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            elif format == 'lab':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            elif format == 'rgb':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        if edit:
            frame = cv.medianBlur(frame, 3)
        if size:
            frame = cv.resize(frame, size)

        min1 = cv.getTrackbarPos('min 1', 'result')
        min2 = cv.getTrackbarPos('min 2', 'result')
        min3 = cv.getTrackbarPos('min 3', 'result')
        max1 = cv.getTrackbarPos('max 1', 'result')
        max2 = cv.getTrackbarPos('max 2', 'result')
        max3 = cv.getTrackbarPos('max 3', 'result')
        
        mask = cv.inRange(frame, (min1, min2, min3), (max1, max2, max3))
        corrected_frame = cv.bitwise_and(frame, frame, mask=mask)
        if edit:
            kernel = np.ones((5, 5), np.uint8)
            eroded = cv.erode(frame, kernel)
            corrected_frame = cv.dilate(eroded, kernel)
        cv.imshow('result', corrected_frame)

        if cv.waitKey(1) == 0xFF:
            if type == 'video':
                cap.release()
                cv.destroyAllWindows()
            break


if __name__ == "__main__":
    # type - input type (by default - video, you can choose 'image')
    # src - video file path (by default 0 - webcam),
    # format - video format (by default 'bgr', you can choose 'rgb', 'hsv', 'lab')
	 # edit - enable/disable filters (by default True)
	 # size - new size of image/video. You can use it шf the top edge of the trackbars extends beyond the window
	 # example: main(type='image', src='./HSV-corrector/assets/sample.jpg', format='hsv')
    main(type='image', src='./18-19-09.jpg')