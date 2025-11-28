import sys
from ui.mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    uiInstance = MainWindow()
    uiInstance.show()
    sys.exit(app.exec_())