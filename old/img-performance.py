import cv2
import numpy as np
import time
import winsound
import DXGI_screen_capture  # pybind11 모듈
DXGI_screen_capture.init()

freud = cv2.imread("freud.png", cv2.IMREAD_COLOR)
freud_gray = cv2.cvtColor(freud, cv2.COLOR_BGR2GRAY)
w, h = freud_gray.shape[::-1]

erda = cv2.imread("erda.png", cv2.IMREAD_COLOR)
erda_gray = cv2.cvtColor(erda, cv2.COLOR_BGR2GRAY)
w, h = erda_gray.shape[::-1]

threshold = 0.963
was_found = False

cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Screen Capture", 800, 600)

while True:
    start = time.time()

    img = DXGI_screen_capture.get_screen_image()
    if img.size == 0:
        continue

    img_bgr = cv2.cvtColor(np.array(img, copy=False), cv2.COLOR_BGRA2BGR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, freud_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    found = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_bgr, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 2)
        found = True
    if found and not was_found:
        print(">>> 프리드 발견!")
        winsound.Beep(750, 300)

    # was_found = found

    res = cv2.matchTemplate(img_gray, erda_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    found = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_bgr, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 2)
        found = True
    if found and not was_found:
        print(">>> 에르다 발견!")
        winsound.Beep(750, 300)

    was_found = found

    cv2.imshow("Screen Capture", img_bgr)

    elapsed = time.time() - start
    time.sleep(max(0, 0.1 - elapsed))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
