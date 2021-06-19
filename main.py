from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import schedulerui


class SchoolScheduler(QtWidgets.QMainWindow, schedulerui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(SchoolScheduler, self).__init__(parent)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    form = SchoolScheduler()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
