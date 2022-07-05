
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QCheckBox,\
    QLineEdit, QLabel, QWidget, QPushButton, QRadioButton


class CoordinateLine(QLineEdit):
    def __init__(self):
        super().__init__()


class CoordinateRadioButton(QRadioButton):
    def __init__(self, name):
        super().__init__(name)
        self.setFixedWidth(50)