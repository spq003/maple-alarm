import sys
import os
import cv2
import time
import copy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QDialog, QRadioButton, QPushButton, QApplication
from PyQt5 import uic

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from capture import CaptureThread
from analysis import TemplateThread

class MainWindow(QDialog):
    default_path = os.path.join(os.path.dirname(__file__), '..')
    methods = {
        "tail": cv2.TM_CCORR_NORMED,
        "erda": cv2.TM_CCOEFF_NORMED,
        "janus": cv2.TM_CCOEFF_NORMED,
        "freud": cv2.TM_CCOEFF_NORMED,
    }
    threshold = {
        "tail": 0.98,
        "erda": 0.95,
        "janus": 0.95,
        "freud": 0.95,
    }
    templates = {
        "tail": cv2.imread(default_path + "/img/tail.png", 0),
        "erda": cv2.imread(default_path + "/img/erda.png", 0),
        "janus": cv2.imread(default_path + "/img/janus.png", 0),
        "freud": cv2.imread(default_path + "/img/freud.png", 0)
    }
    
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'mainWindow.ui')
        uic.loadUi(ui_path, self)

        self.imageLabel = self.findChild(QLabel, "imageLabel")
        self.radioButton1 = self.findChild(QRadioButton, "radioButton1")
        self.radioButton2 = self.findChild(QRadioButton, "radioButton2")
        self.radioButton3 = self.findChild(QRadioButton, "radioButton3")
        self.radioButton4 = self.findChild(QRadioButton, "radioButton4")
        self.applyButton = self.findChild(QPushButton, "applyButton")
        self.applyButton.clicked.connect(self._apply_click)
        self.detected_box = None
        self.detected_time = time.time()
        self.BOX_HOLD_TIME_MS = 300

        self.captureThread = CaptureThread()
        self.captureThread.frame_ready.connect(self.update_frame)
        self.captureThread.start()

        self.templateThread = TemplateThread(self.templates, self.threshold, self.methods)
        self.templateThread.result_ready.connect(self.handle_template_result)
        self.captureThread.frame_ready.connect(self.templateThread.update_frame)
        self.templateThread.start()

    def handle_template_result(self, result):
        status = result["status"]
        x, y, w, h = result["box"]
        conf = result["confidence"]
        # if conf < 0.9:
        #     return
        print(f'>> {status}: {conf}')
        self.detected_box = (x, y, w, h)
        self.detected_time = time.time()

    def update_frame(self, frame):
        new_frame = self.draw_box(frame)

        h, w, c = new_frame.shape
        qImg = QImage(new_frame.data.tobytes(), w, h, c*w, QImage.Format_BGR888)
        self.imageLabel.setPixmap(QPixmap.fromImage(qImg).scaled(641, 361))

    def draw_box(self, frame):
        my_frame = copy.deepcopy(frame) # 박스 표시용 frame 새로 생성
        box = self.detected_box # 지역변수로 복사해서 체크
        if box is None: return frame

        if (time.time() - self.detected_time) * 1000 < self.BOX_HOLD_TIME_MS:
            x, y, w, h = box
            cv2.rectangle(my_frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
        else:
            self.detected_box = None
        return my_frame

    def close_event(self, event):
        self.captureThread.stop()
        self.templateThread.stop()
        event.accept()

    def _apply_click(self):
        if self.radioButton1.isChecked():
            self.templateThread.set_status("tail")
        elif self.radioButton2.isChecked():
            self.templateThread.set_status("erda")
        elif self.radioButton3.isChecked():
            self.templateThread.set_status("janus")
        elif self.radioButton4.isChecked():
            self.templateThread.set_status("freud")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    uiInstance = MainWindow()
    uiInstance.show()
    sys.exit(app.exec_())