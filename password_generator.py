import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QSlider, QSpinBox, QGridLayout
from PyQt6.QtCore import Qt
import random
import string

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.spin = QSpinBox()
        self.copy_btn = QPushButton("Copy")
        self.btn_lower = QPushButton("a-z")
        self.btn_upper = QPushButton("A-Z")
        self.btn_digits = QPushButton("0-9")
        self.btn_symbols = QPushButton("#$%")
        self.line_for_passwords = QLineEdit()

        self.btn_lower.clicked.connect(lambda: self.toggle_character_set('lower'))
        self.btn_upper.clicked.connect(lambda: self.toggle_character_set('upper'))
        self.btn_digits.clicked.connect(lambda: self.toggle_character_set('digits'))
        self.btn_symbols.clicked.connect(lambda: self.toggle_character_set('symbols'))

        layout.addWidget(self.spin, 2, 2, 1, 1)
        layout.addWidget(self.slider, 2, 1, 1, 1)
        layout.addWidget(self.line_for_passwords, 1, 1, 1, 1)
        layout.addWidget(self.btn_lower, 3, 1, 1, 1)
        layout.addWidget(self.btn_upper, 3, 2, 1, 1)
        layout.addWidget(self.btn_digits, 3, 3, 1, 1)
        layout.addWidget(self.btn_symbols, 3, 4, 1, 1)
        layout.addWidget(self.copy_btn, 4, 1, 1, 4)

        new_page = QWidget()
        new_page.setLayout(layout)
        self.main_content.addWidget(new_page)

        self.setLayout(layout)
        self.setWindowTitle('Password Generator')

        self.btn_lower.setCheckable(True)
        self.btn_upper.setCheckable(True)
        self.btn_digits.setCheckable(True)
        self.btn_symbols.setCheckable(True)

        self.generate_password()

    def toggle_character_set(self, set_name):
        if set_name == 'lower':
            self.btn_lower.toggle()
        elif set_name == 'upper':
            self.btn_upper.toggle()
        elif set_name == 'digits':
            self.btn_digits.toggle()
        elif set_name == 'symbols':
            self.btn_symbols.toggle()

        self.generate_password()

    def generate_password(self):
        password_length = self.spin.value()
        characters = ""

        if self.btn_lower.isChecked():
            characters += string.ascii_lowercase
        if self.btn_upper.isChecked():
            characters += string.ascii_uppercase
        if self.btn_digits.isChecked():
            characters += string.digits
        if self.btn_symbols.isChecked():
            characters += "#$%"

        if not characters:
            characters = string.ascii_letters + string.digits

        generated_password = ''.join(random.choice(characters) for _ in range(password_length))
        self.line_for_passwords.setText(generated_password)

