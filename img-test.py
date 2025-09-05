import cv2
import numpy as np
import DXGI_screen_capture  # pybind11 모듈
DXGI_screen_capture.init()
# 찾고자 하는 이미지 (100px 내외)
template = cv2.imread("freud.png", cv2.IMREAD_COLOR)
w, h = template.shape[1], template.shape[0]

# OpenCV 창 설정
cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Screen Capture", 800, 600)

threshold = 0.9  # 유사도 기준 0~1, 0.9 정도가 안전

while True:
    # 화면 캡처
    img = DXGI_screen_capture.get_screen_image()
    if img.size == 0:
        continue
    
    img_bgr = cv2.cvtColor(np.array(img, copy=False), cv2.COLOR_BGRA2BGR)
    
    # 템플릿 매칭
    res = cv2.matchTemplate(img_bgr, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    # 탐지 시 알림
    detected = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_bgr, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 2)
        detected = True
    
    if detected:
        print(">>> 이미지 발견!")
    
    # 화면 표시
    cv2.imshow("Screen Capture", img_bgr)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
