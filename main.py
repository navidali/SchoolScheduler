import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

import schedulerui
from schedule import *
from wsl import *


class SchoolScheduler(QtWidgets.QMainWindow, schedulerui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(SchoolScheduler, self).__init__(parent)
        self.setupUi(self)




def start_gui():
    app = QApplication(sys.argv)
    form = SchoolScheduler()
    form.show()
    app.exec_()


def main():
    # UI
    set_display_to_host()
    start_gui()


if __name__ == '__main__':
    # purge fixes fresh start up bug
    # TODO REMOVE COMMENT OUT TO ALLOW PURGE
    db_purge()

    db_init()
    main()
    db_close()
