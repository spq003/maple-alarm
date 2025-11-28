import win32gui
import cv2
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

import core.DXGI_screen_capture as eye

class CaptureThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__()
        self.running = True
        eye.init()

    def run(self):
        while self.running:
            try:
                capture = self.maple_screen_capture()
                self.frame_ready.emit(capture)
            except: # 캡쳐 중 오류 발생시 프레임 스킵
                continue
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

        try:
            hwnd = win32gui.FindWindow(None, "MapleStory") # 창 핸들 가져오기
            rect = win32gui.GetWindowRect(hwnd) # 창 좌표 가져오기
            if max(rect) < 0: # 창 좌표를 찾을 수 없는경우 전체화면 반환
                return img
        except:
            return img

        left = max(0, rect[0])
        top = max(0, rect[1])
        right = min(img.shape[1], rect[2])
        bottom = min(img.shape[0], rect[3])
        img = img[top:bottom, left:right]
        return img