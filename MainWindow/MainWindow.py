from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QWidget, QGridLayout, QLabel, QPushButton, \
    QMessageBox, QSlider, QSpinBox, QTextEdit, \
    QApplication, QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox, QVBoxLayout
import random
import string
import sys
from Forms.MainWindowForm import Ui_MainWindow_2
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette
from PyQt6 import QtWidgets, QtGui, QtCore
from Generator_paroleiForm import PasswordGenerator
from check_second_db import CheckThreadSecond
import sqlite3
from passwords.code_for_db import create_table
import os
from FormForPasswordGenerator import Ui_MainWindow_3

connection = sqlite3.connect("passwords/db_for_passwords.db")
cursor = connection.cursor()
query = "SELECT * FROM db_for_passwords"
cursor.execute(query)
data = cursor.fetchall()
create_table()
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'passwords', 'db_for_passwords.db')



class MainWindowPasswords(QMainWindow, Ui_MainWindow_2):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_MainWindow_2()
        self.ui.setupUi(self)
        self.setWindowTitle("Main Window")
        self.setStyleSheet('background-color: darkgrey;')


        self.title_label = self.ui.title_label
        self.title_label.setText("Second Window")

        self.title_icon = self.ui.title_icon
        self.title_icon.setText("")
        self.title_icon.setPixmap(QPixmap("password_3715.png"))
        self.title_icon.setScaledContents(True)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only = self.ui.listWidget_iconOnly
        self.side_menu_icon_only.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only.hide()

        self.menu_btn = self.ui.pushButton
        self.menu_btn.setObjectName("menu_btn")
        self.menu_btn.setText("")
        self.menu_btn.setIcon(QIcon("MainWindow/4115230-cancel-close-cross-delete_114048.svg"))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setChecked(False)


        self.main_content = self.ui.stackedWidget



        self.menu_list =[
            {
                "name": "Home",
                "icon": "MainWindow/home.svg"
            },
            {
                "name": "Passwords",
                "icon": "MainWindow/password_icon.svg"
            },
            {
                "name": "Generator Passwords",
                "icon": "MainWindow/generator_passwords.svg"
            },
            {
                "name": "New Password",
                "icon": "MainWindow/users_group_customers_clients_icon-icons.com_72448.svg"
            },
            {
                "name": "Reports",
                "icon": "MainWindow/reports_clipboard_examboard_checklist_report_icon_191169.svg"
            },
            {
                "name": "Exit",
                "icon": "MainWindow/exit.svg"
            }

        ]



        self.init_list_widget()
        self.init_signal_slot()
        self.init_stackwidget()






    def init_signal_slot(self):
        self.menu_btn.toggled.connect(self.side_menu.setHidden)
        self.menu_btn.toggled.connect(self.title_label.setHidden)
        self.menu_btn.toggled.connect(self.title_icon.setHidden)
        self.menu_btn.toggled.connect(self.side_menu_icon_only.setVisible)

        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu.currentRowChanged['int'].connect(self.side_menu_icon_only.setCurrentRow)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.side_menu.setCurrentRow)

        self.menu_btn.toggled.connect(self.button_icon_changed)


    def button_icon_changed(self, status):
        if status:
            self.menu_btn.setIcon(QIcon("MainWindow/openfolderwithfile_122800.svg"))
        else:
            self.menu_btn.setIcon(QIcon("MainWindow/4115230-cancel-close-cross-delete_114048.svg"))


    def init_list_widget(self):
        self.side_menu.clear()
        self.side_menu_icon_only.clear()

        
        for menu in self.menu_list:
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setSizeHint(QSize(40, 40))
            self.side_menu_icon_only.addItem(item)
            self.side_menu_icon_only.setCurrentRow(0)


            item_new = QListWidgetItem()
            item_new.setIcon(QIcon(menu.get("icon")))
            item_new.setText(menu.get("name"))
            self.side_menu.addItem(item_new)
            self.side_menu.setCurrentRow(0)


    def init_stackwidget(self):
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        for menu in self.menu_list:
            text = menu.get("name")
            layout = QGridLayout()
            
            label = QLabel(text=text)
            font = QFont()
            font.setPixelSize(20)
            label.setFont(font)
            layout.addWidget(label, 0, 0, 0, 0)


            if text == "Exit":
                exit_button = QPushButton("Exit")
                label.setStyleSheet("font-size: 20px;"
                                    "font-weight: bold;")
                exit_button.clicked.connect(self.exit_func)
                exit_button.setStyleSheet("background-color: lightblue;"
                                          "border: 2px solid darkblue;"
                                          "border-radius: 5px;"
                                          "padding: 5px;")
                layout.addWidget(label,0,0)
                layout.addWidget(exit_button,1,0)





            if text == "Generator Passwords":
                label.setStyleSheet("font-size: 20px;"
                                    "font-weight: bold;")
                self.length_label = QLabel('Password Length:')
                self.length_input = QLineEdit(self)
                self.length_input.setValidator(QtGui.QIntValidator())

                self.uppercase_checkbox = QCheckBox('Uppercase')
                self.lowercase_checkbox = QCheckBox('Lowercase')
                self.digits_checkbox = QCheckBox('Digits')
                self.symbols_checkbox = QCheckBox('Symbols')

                self.generated_password_label = QLabel('Generated Password:')
                self.generated_password_output = QLineEdit(self)
                self.generated_password_output.setReadOnly(True)




                self.gridLayout = QtWidgets.QGridLayout()
                self.gridLayout.setObjectName("gridLayout")

                self.generate_button = QPushButton('Generate Password')
                self.generate_button.clicked.connect(self.generate_password)
                self.generate_button.setStyleSheet("background-color: lightgreen;"
                                       "border: 2px solid green;"
                                       "border-radius: 5px;"
                                       "padding: 5px;")





                layout.addWidget(label, 0, 0)
                layout.addWidget(self.length_label, 1, 0)
                layout.addWidget(self.length_input, 1, 1)
                layout.addWidget(self.uppercase_checkbox, 2, 0)
                layout.addWidget(self.lowercase_checkbox, 2, 1)
                layout.addWidget(self.digits_checkbox, 3, 0)
                layout.addWidget(self.symbols_checkbox, 3, 1)
                layout.addWidget(self.generated_password_output, 4, 0, 1, 2)
                layout.addWidget(self.generate_button, 5, 0, 1, 2)
                layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)






            if text == "Reports":
                label.setText("Write your report")
                label.setAlignment(Qt.AlignmentFlag.AlignTop)
                label.setStyleSheet("font-size: 20px;"
                                    "font-weight: bold;")
                layout.addWidget(label)
                self.text_box = QTextEdit()

                self.text_box.setPlaceholderText("Write your report")
                btn_send = QPushButton("Send Report")
                btn_send.clicked.connect(self.send_report)
                btn_send.setStyleSheet("background-color: lightblue;"
                                          "border: 2px solid darkblue;"
                                          "border-radius: 5px;"
                                          "padding: 5px;")
                layout.addWidget(label, 0, 0)
                layout.addWidget(self.text_box, 1, 0)
                layout.addWidget(btn_send, 2,0)



            if text == "New Password":
                label.setText("Form \n to make new password")
                layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                label.setStyleSheet("font-size: 20px;"
                                    "font-weight: bold;")
                self.line_edit_name = QLineEdit()
                self.line_edit_name.setPlaceholderText("Write name")
                self.line_edit_password = QLineEdit()
                self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
                self.line_edit_password.setPlaceholderText("Write password")
                self.info_box = QLineEdit()
                self.info_box.setMaximumSize(600, 200)
                self.info_box.setPlaceholderText("Write info(website, ect..)")
                self.btn_new_password = QPushButton("Submit")
                self.btn_new_password.setStyleSheet("background-color: black;"
                                          "border: 2px solid darkblue;"
                                          "border-radius: 5px;"
                                          "padding: 5px;")

                layout.addWidget(self.line_edit_name, 1, 1)
                layout.addWidget(self.line_edit_password, 2, 1)
                layout.addWidget(self.info_box, 3, 1)
                layout.addWidget(self.btn_new_password, 4, 1)
                layout.addWidget(label, 0, 1)

                self.btn_new_password.clicked.connect(self.new_password)
                self.base_line_edit_second = [self.line_edit_name, self.line_edit_password, self.info_box]

                self.check_second_db = CheckThreadSecond()
                self.check_second_db.mysignalsecond.connect(self.signal_handler_second)


            if text == "Home":
                label.setAlignment(Qt.AlignmentFlag.AlignTop)
                label.setStyleSheet("font-size: 20px;"
                                    "font-weight: bold;")
                widget = QLabel()


                widget.setPixmap(QPixmap('MainWindow/password_120207.svg'))
                widget.setFixedSize(QSize(40, 40))
                text_for_home = QLabel("Welcome to SecurePass Manager – Your Trusted Partner in Password Security!\nIn today's digital age, safeguarding your online presence is paramount. As we navigate a world filled with numerous accounts,\n"
                                       " each requiring a unique and robust password, managing them all can become a daunting task.\n "
                                       )
                text_for_home.setStyleSheet("color: white;"
                                            )
                text_for_home.setMaximumSize(800, 65)
                text_for_home2 = QLabel("Why Choose SecurePass Manager?")
                text_for_home2.setStyleSheet("color: white;"
                                            )
                text_for_home3 = QLabel("1. Simplified Security:\n"
                                           "No more sticky notes or Excel sheets filled with passwords. SecurePass Manager simplifies your digital life by securely storing and organizing all your passwords in one centralized location.\n")
                text_for_home3.setMaximumSize(800, 65)
                text_for_home3.setStyleSheet("color: white;"
                                             )
                text_for_home4 = QLabel("2. Bank-Grade Encryption:\n"
                                           "Your security is our top priority. With state-of-the-art encryption protocols, rest assured that your sensitive information is locked down with the same level of protection used by financial institutions.\n")
                text_for_home4.setMaximumSize(800, 65)
                text_for_home4.setStyleSheet("color: white;"
                                             )
                text_for_home5 = QLabel("3. Cross-Platform Accessibility:\n"
                                           "Access your passwords anytime, anywhere. Whether you're on your computer, tablet, or smartphone, SecurePass Manager syncs seamlessly across all your devices.\n")
                text_for_home5.setMaximumSize(800, 65)
                text_for_home5.setStyleSheet("color: white;"
                                             )
                text_for_home6 = QLabel("4. Password Generator:\n"
                                           "Tired of coming up with complex passwords? Our built-in password generator creates strong, unique passwords for each of your accounts, enhancing your overall digital security.")
                text_for_home6.setMaximumSize(800, 65)
                text_for_home6.setStyleSheet("color: white;"
                                             )
                layout.addWidget(label, 1, 0)
                layout.addWidget(widget, 0, 0)

                layout.addWidget(text_for_home, 2, 0)
                layout.addWidget(text_for_home2, 3, 0)
                layout.addWidget(text_for_home3, 4, 0)
                layout.addWidget(text_for_home4, 5, 0)
                layout.addWidget(text_for_home5, 6, 0)
                layout.addWidget(text_for_home6, 7, 0)
                layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)




            if text == "Passwords":
                cursor.execute("SELECT * FROM db_for_passwords")
                data = cursor.fetchall()
                self.tableWidget = QTableWidget()
                self.tableWidget.setColumnCount(3)
                self.btn_update_table = QPushButton("Update Table")
                self.btn_update_table.clicked.connect(self.update_table)
                self.btn_update_table.setStyleSheet("background-color: black;"
                                                    "border: 2px solid gray;"
                                                    "border-radius: 5px;"
                                                    "padding: 5px;")



                headers = [description[0] for description in cursor.description]
                self.tableWidget.setHorizontalHeaderLabels(headers)
                for row_num, row_data in enumerate(data):
                    self.tableWidget.insertRow(row_num)
                    for col_num, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        self.tableWidget.setItem(row_num, col_num, item)

                layout.addWidget(self.tableWidget, 0,0)
                layout.addWidget(self.btn_update_table, 0, 1)







            new_page = QWidget()
            new_page.setLayout(layout)
            self.main_content.addWidget(new_page)

    def generate_password(self):
        length_text = self.length_input.text()

        if not length_text:
            self.generated_password_output.setText('Please enter a password length.')
            return

        length = int(length_text)
        use_uppercase = self.uppercase_checkbox.isChecked()
        use_lowercase = self.lowercase_checkbox.isChecked()
        use_digits = self.digits_checkbox.isChecked()
        use_symbols = self.symbols_checkbox.isChecked()

        chars = ''
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation

        if not chars:
            self.generated_password_output.setText('Please select at least one character type.')
        else:
            password = ''.join(random.choice(chars) for _ in range(length))
            self.generated_password_output.setText(password)


    def check_input_second(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit_second:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper


    def signal_handler_second(self, value):
        QtWidgets.QMessageBox.about(self, 'Warning', value)


    @check_input_second
    def new_password(self):
        name_second = self.line_edit_name.text()
        password_second = self.line_edit_password.text()
        info_second = self.info_box.text()
        self.check_second_db.thr_register_second(name_second, password_second, info_second)
        self.line_edit_password.setText('')
        self.line_edit_name.setText('')
        self.info_box.setText('')

    def update_table(self):
        self.tableWidget.setRowCount(0)

        cursor.execute("SELECT * FROM db_for_passwords")
        data = cursor.fetchall()

        for row_num, row_data in enumerate(data):
            self.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_num, col_num, item)




    def send_report(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Report")
        dlg.setText("Your report has been sent")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes )
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
        self.text_box.setText("")
        if button == QMessageBox.StandardButton.Yes:
            pass


    def exit_func(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Exit")
        dlg.setText("Are you sure you want to exit?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.close()










