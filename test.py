import cv2
import numpy as np

# 창 이름 지정 및 크기 조절 가능 옵션 설정
cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)  # 크기 조절 가능
cv2.resizeWindow("Screen Capture", 800, 600)          # 원하는 크기로 설정

# 1. DLL 경로 추가
# sys.path.append(r"C:\Users\spq00\source\repos\DXIG_screen_capture\x64\Debug")

# 2. pybind11 모듈 import
import DXGI_screen_capture

# 3. 초기화
# init() 함수가 있으면 호출
DXGI_screen_capture.init()  # 만약 C++ 쪽 init()을 pybind11로 바인딩했다면 호출

# 4. 화면 캡처 반복
while True:
    img = DXGI_screen_capture.get_screen_image()
    
    if img.size == 0:
        # 프레임 가져오기 실패
        continue

    # NumPy 배열 → OpenCV BGR 변환
    img_bgr = cv2.cvtColor(np.array(img, copy=False), cv2.COLOR_BGRA2BGR)

    cv2.imshow("Screen Capture", img_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
