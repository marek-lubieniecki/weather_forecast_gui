# Filename: signals_slots.py

"""Signals and slots example."""

import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QGridLayout, QLineEdit, QLabel, QWidget
#from GfsClasses import Gfs

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My app")
        self.UiComponents()

    def UiComponents(self):
        layout = QVBoxLayout()
        coordinate_layout = QGridLayout()
        CentralWidget = QWidget()
        ForecastDatePicker = QCalendarWidget()
        #coordinate_label =

        LatitudeLine = QLineEdit()
        LongitudeLine = QLineEdit()



        layout.addWidget(QLabel("Select coordinates:"))
        layout.addWidget(LatitudeLine)
        layout.addWidget(LongitudeLine)
        layout.addWidget(ForecastDatePicker)
        CentralWidget.setLayout(layout)
        self.setCentralWidget(CentralWidget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
