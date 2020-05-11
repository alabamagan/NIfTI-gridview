from ngv_gui import ngv_mainwindow
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ngv_mainwindow()
    window.show()

    sys.exit(app.exec_())