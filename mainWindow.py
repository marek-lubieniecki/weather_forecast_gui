import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QButtonGroup, QLineEdit, QLabel, QWidget, QPushButton, QMessageBox
from mapWindow import *

from widgetConfig import *
from utility import *

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

        self.latitude_button_group = QButtonGroup()
        self.latitude_layout = QHBoxLayout(self)
        self.latitude_line = CoordinateLine()
        self.north_checkbox = CoordinateRadioButton("North")
        self.south_checkbox = CoordinateRadioButton("South")
        self.latitude_button_group.addButton(self.north_checkbox)
        self.latitude_button_group.addButton(self.south_checkbox)
        self.latitude_layout.addWidget(self.latitude_line)
        self.latitude_layout.addWidget(self.north_checkbox)
        self.latitude_layout.addWidget(self.south_checkbox)

        self.longitude_button_group = QButtonGroup()
        self.longitude_layout = QHBoxLayout(self)
        self.longitude_line = CoordinateLine()
        self.east_checkbox = CoordinateRadioButton("East")
        self.west_checkbox = CoordinateRadioButton("West")
        self.longitude_button_group.addButton(self.east_checkbox)
        self.longitude_button_group.addButton(self.west_checkbox)
        self.longitude_layout.addWidget(self.longitude_line)
        self.longitude_layout.addWidget(self.east_checkbox)
        self.longitude_layout.addWidget(self.west_checkbox)

        self.longitude_line.setText("0.00")
        self.latitude_line.setText("0.00")
        self.north_checkbox.setChecked(1)
        self.east_checkbox.setChecked(1)

        self.longitude_line.textChanged.connect(self.update_coordinates_label)
        self.latitude_line.textChanged.connect(self.update_coordinates_label)


        self.coordinates_rounded_label = QLabel()
        show_map_button = QPushButton("Show location on map")
        show_map_button.setCheckable(True)
        show_map_button.clicked.connect(self.showMap)

        self.download_forecast_button = QPushButton("Download")
        self.show_forecast_button = QPushButton("Show")
        self.button_layout = QHBoxLayout(self)

        self.button_layout.addWidget(self.download_forecast_button)
        self.button_layout.addWidget(self.show_forecast_button )

        layout.addWidget(QLabel("Latitude:"))
        layout.addLayout(self.latitude_layout)
        layout.addWidget(QLabel("Longitude:"))
        layout.addLayout(self.longitude_layout)
        layout.addWidget(self.coordinates_rounded_label)
        layout.addWidget(show_map_button)
        layout.addWidget(forecast_date_picker)
        layout.addLayout(self.button_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.latitude = 0
        self.longitude = 0
        self.latitude_round = 0
        self.longitude_round = 0

    def showMap(self):
        pass

    def update_coordinates_label(self):
        self.latitude = self.latitude_line.text()
        self.longitude = self.longitude_line.text()

        try:
            self.latitude_round = round_coordinates(float(self.latitude))
            self.longitude_round = round_coordinates(float(self.longitude))
        except Exception:
            QMessageBox.about(self, 'Error', 'Input a number')
        self.coordinates_rounded_label.setText('Current coordinates: ' + str(self.latitude_round) + ' ' + str(self.longitude_round))


