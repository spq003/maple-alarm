import cv2
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

class TemplateThread(QThread):
    result_ready = pyqtSignal(dict)  
    # ex) {"status": "attack", "box": (x,y,w,h), "confidence": 0.94}

    def __init__(self, templates: dict):
        """
        templates = {
            "erda": cv2.imread("img/erda.png", 0),
            "freud": cv2.imread("img/freud.png", 0),
            "tail": cv2.imread("img/tail.png", 0)
        }
        """
        super().__init__()
        self.templates = templates
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
            
            template = self.templates[self.current_status]
            if template is None:
                self.msleep(10)
                continue

            gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val < 0.9: continue
            th, tw = template.shape[:2]
            x, y = max_loc

            self.result_ready.emit({
                "status": self.current_status,
                "box": (x, y, tw, th),
                "confidence": float(max_val)
            })

            self.msleep(10)
