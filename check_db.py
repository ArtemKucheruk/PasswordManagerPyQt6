from PyQt6 import QtCore
from handler.db_handler import *

class CheckThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def thr_login(self, name, password):
        login(name, password, self.mysignal)

    def thr_reg(self, name, password):
        reg(name, password, self.mysignal)