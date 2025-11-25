import sys
import os
import cv2
import time
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QDialog, QRadioButton, QPushButton, QApplication
from PyQt5 import uic

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from capture import CaptureThread
from analysis import TemplateThread

class MainWindow(QDialog):
    """
    QRadioButton radioButton1 : 악몽선경
    QRadioButton radioButton2 : 솔에르다
    QRadioButton radioButton3 : 솔야누스
    QRadioButton radioButton4 : 프리드
    QPushButton applyButton
    QLabel imageLabel
    """
    
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
        self.detected_time = 0
        self.BOX_HOLD_TIME_MS = 300

        self.captureThread = CaptureThread()
        self.captureThread.frame_ready.connect(self.update_frame)
        self.captureThread.start()

        default_path = os.path.join(os.path.dirname(__file__), '..')
        templates = {
            "tail": cv2.imread(default_path + "/img/tail.png", 0),
            "erda": cv2.imread(default_path + "/img/erda.png", 0),
            "erda2": cv2.imread(default_path + "/img/erda.png", 0),
            "freud": cv2.imread(default_path + "/img/freud.png", 0)
        }
        self.templateThread = TemplateThread(templates)
        self.templateThread.result_ready.connect(self.handle_template_result)
        self.captureThread.frame_ready.connect(self.templateThread.update_frame)
        self.templateThread.start()

    def handle_template_result(self, result):
        status = result["status"]
        x, y, w, h = result["box"]
        conf = result["confidence"]
        #print(f"[{status}] matched at {x,y} conf={conf}")
        self.detected_box = (x, y, w, h)
        self.detected_time = time.time()

    def _apply_click(self):
        if self.radioButton1.isChecked():
            self.templateThread.set_status("tail")
        elif self.radioButton2.isChecked():
            self.templateThread.set_status("erda")
        elif self.radioButton3.isChecked():
            self.templateThread.set_status("erda2")
        elif self.radioButton4.isChecked():
            self.templateThread.set_status("freud")

    def update_frame(self, frame):
        box_draw_frame = frame
        if self.detected_box is not None:
            if ((time.time() - self.detected_time) * 1000) < self.BOX_HOLD_TIME_MS:
                x, y, w, h = self.detected_box
                cv2.rectangle(box_draw_frame, (x, y), (x + w, y + h), (0, 0, 255), 10)
            else:
                self.detected_box = None

        h, w, c = frame.shape
        qImg = QImage(frame.data.tobytes(), w, h, c*w, QImage.Format_BGR888)
        self.imageLabel.setPixmap(QPixmap.fromImage(qImg).scaled(641, 361))

    def close_event(self, event):
        self.captureThread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    uiInstance = MainWindow()
    uiInstance.show()
    sys.exit(app.exec_())