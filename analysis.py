import cv2
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

class TemplateThread(QThread):
    result_ready = pyqtSignal(dict) # {"status": "tail", "box": (x,y,w,h), "confidence": 0.94}

    def __init__(self, templates: dict, thresholds: dict, methods: dict):
        super().__init__()
        self.templates = templates
        self.thresholds = thresholds
        self.methods = methods
        self.current_status = None
        self.running = True
        self.frame = None

    def update_frame(self, frame): # CaptureThread → TemplateThread로 프레임 전달
        self.frame = frame

    def set_status(self, status: str): # MainWindow → TemplateThread로 상태 전달
        if status in self.templates:
            self.current_status = status

    def run(self):
        while self.running:
            if (self.frame is None) or (self.current_status is None):
                self.msleep(10)
                continue
            gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            template = self.templates[self.current_status]

            res = cv2.matchTemplate(gray_frame, template, self.methods[self.current_status]) # method: cv2.TM_~~~
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            th, tw = template.shape[:2]
            res_vals = (max_val, max_loc[0], max_loc[1], tw, th) # {conf, x, y, w, h}
            
            if res_vals[0] < self.thresholds[self.current_status]:
                continue

            self.result_ready.emit({
                    "status": self.current_status,
                    "box": (res_vals[1], res_vals[2], res_vals[3], res_vals[4]),
                    "confidence": float(res_vals[0])
            })
            self.msleep(20)

    def stop(self):
        self.running = False
        self.wait()
