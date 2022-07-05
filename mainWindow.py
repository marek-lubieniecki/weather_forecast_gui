import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QCheckBox, QLineEdit, QLabel, QWidget, QPushButton
from mapWindow import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GFS Weather Forecast GUI")
        self.UiComponents()

    def UiComponents(self):
        layout = QVBoxLayout()
        coordinate_layout = QHBoxLayout()
        central_widget = QWidget()
        forecast_date_picker = QCalendarWidget()

        latitude_layout = QHBoxLayout()
        latitude_line = QLineEdit()
        latitude_line.setInputMask('00.000000')
        north_checkbox = QCheckBox("North")
        south_checkbox = QCheckBox("South")
        latitude_layout.addWidget(latitude_line)
        latitude_layout.addWidget(north_checkbox)
        latitude_layout.addWidget(south_checkbox)

        longitude_layout = QHBoxLayout()
        longitude_line = QLineEdit()
        longitude_line.setInputMask('00.000000')

        show_map_button = QPushButton("Show location on map")
        show_map_button.setCheckable(True)
        show_map_button.clicked.connect(self.showMap)

        latitude_layout.addWidget(latitude_line)

        layout.addWidget(QLabel("Latitude:"))
        layout.addLayout(latitude_layout)
        layout.addWidget(QLabel("Longitude:"))
        layout.addWidget(longitude_line)
        layout.addWidget(show_map_button)
        layout.addWidget(forecast_date_picker)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def showMap(self):
        pass

    def
