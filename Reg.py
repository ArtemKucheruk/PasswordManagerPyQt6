import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from check_db import CheckThread
from Forms.SignInform import Ui_MainWindow
from MainWindow.MainWindow import MainWindowPasswords


class Interface(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet('background-color: darkgrey;')

        self.ui.pushButton.clicked.connect(self.auth)
        self.ui.pushButton.setStyleSheet("border: 2px solid black;"
                                            "border-radius: 5px;"
                                            "padding: 5px;")
        self.ui.pushButton_2.clicked.connect(self.reg)
        self.ui.pushButton_2.setStyleSheet("border: 2px solid black;"
                                         "border-radius: 5px;"
                                         "padding: 5px;")

        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]
        self.ui.lineEdit.setStyleSheet("background-color:black")
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ui.lineEdit_2.setStyleSheet("background-color:black")

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)

    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper

    def signal_handler(self, value):
        if value == "Login success":
            self.open_second_window()
        else:
            QtWidgets.QMessageBox.about(self, "Оповищение", value)

    def open_second_window(self):
        username = self.ui.lineEdit.text()
        self.main_window = MainWindowPasswords(username)
        self.main_window.show()
        self.close()

    @check_input
    def auth(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()

        self.check_db.thr_login(name, passw)

    @check_input
    def reg(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_reg(name, passw)

app = QApplication(sys.argv)
w = Interface()
w.show()
app.exec()