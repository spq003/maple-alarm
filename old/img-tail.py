import cv2
import numpy as np
import DXGI_screen_capture  # pybind 모듈
import winsound
import time

DXGI_screen_capture.init() # pybind

template = cv2.imread("tail.png", cv2.IMREAD_COLOR)
w, h = template.shape[1], template.shape[0]

cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)

threshold = 0.98
last_detected_boxes = []

while True:
    img = DXGI_screen_capture.get_screen_image()
    if img.size == 0:
        continue
    img_bgr = cv2.cvtColor(np.array(img, copy=False), cv2.COLOR_BGRA2BGR)
    
    res = cv2.matchTemplate(img_bgr, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    detected = False
    new_boxes = []
    for pt in zip(*loc[::-1]):
        new_boxes.append((pt[0], pt[1], pt[0]+w, pt[1]+h))
        detected = True
    
    if detected:
        last_detected_boxes = new_boxes
        print(">> 이미지 발견")
        winsound.Beep(750, 100) #굳이싶다?

    for box in last_detected_boxes:
        cv2.rectangle(img_bgr, (box[0], box[1]), (box[2], box[3]), (0, 255, 255), 3)
    
    cv2.imshow("Screen Capture", img_bgr)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
