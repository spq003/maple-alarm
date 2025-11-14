import win32gui
import ctypes
import cv2
import numpy as np

import DXGI_screen_capture as eye

eye.init()

while True:
    frame = eye.get_screen_image()
    print(frame is None)
    if frame.size == 0:
        continue

    img = cv2.cvtColor(np.array(frame, copy=False), cv2.COLOR_BGRA2BGR)


    # 창 핸들 가져오기
    hwnd = win32gui.FindWindow(None, "MapleStory")
    print(f'hwnd: {hwnd}')

    # 창 좌표 가져오기
    rect = win32gui.GetWindowRect(hwnd)
    print(f'rect: {rect}')

    left = max(0, rect[0])
    top = max(0, rect[1])
    right = min(img.shape[1], rect[2])
    bottom = min(img.shape[0], rect[3])
    img = img[top:bottom, left:right]

    cv2.imshow("window", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()