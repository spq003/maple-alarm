import win32gui
import cv2
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

import DXGI_screen_capture as eye

class CaptureThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__()
        self.running = True
        eye.init()

    def run(self):
        while self.running:
            maple_frame = self.maple_screen_capture()
            self.frame_ready.emit(maple_frame)
            # print(maple_frame)
            time.sleep(0.02)

    def stop(self):
        self.running = False
        self.wait()

    def full_screen_capture(self):
        frame = eye.get_screen_image()
        if frame.size == 0: return 0
        img = cv2.cvtColor(np.array(frame, copy=False), cv2.COLOR_BGRA2BGR)
        return img

    def maple_screen_capture(self):
        img = self.full_screen_capture()

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
        return img


if __name__ == "__main__":
    while True:
        frame = eye.get_screen_image()
        print(frame is None)
        if frame.size == 0:
            continue

        img = cv2.cvtColor(np.array(frame, copy=False), cv2.COLOR_BGRA2BGR)


        # 창 핸들 가져오기
        hwnd = win32gui.FindWindow(None, "MapleStor2y")
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