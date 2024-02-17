from PyQt6 import QtCore

from passwords.code_for_db import create_table, register_second


class CheckThreadSecond(QtCore.QThread):
    mysignalsecond = QtCore.pyqtSignal(str)

    def thr_register_second(self, password_second, name_second, info_second):
        create_table()
        register_second(password_second,name_second, info_second, self.mysignalsecond)