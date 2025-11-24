import sys
import os
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QDialog, QApplication
from PyQt5 import uic

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from capture import CaptureThread

class MainWindow(QDialog):
    
    

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'mainWindow.ui')
        uic.loadUi(ui_path, self)

        self.imageLabel = self.findChild(QLabel, "imageLabel")

        self.captureThread = CaptureThread()
        self.captureThread.frame_ready.connect(self.update_frame)
        self.captureThread.start()

    def update_frame(self, frame):
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