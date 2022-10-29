import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QButtonGroup, QLineEdit, QLabel, QWidget, QPushButton, QMessageBox
from mapWindow import *

from widgetConfig import *
from utility import *
import geopandas as gpd
import matplotlib.pyplot as plt
from rocketpy import Environment


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

        latitude_button_group = QButtonGroup()
        latitude_layout = QHBoxLayout()
        latitude_line = CoordinateLine()
        north_checkbox = CoordinateRadioButton("North")
        south_checkbox = CoordinateRadioButton("South")
        latitude_button_group.addButton(north_checkbox)
        latitude_button_group.addButton(south_checkbox)
        latitude_layout.addWidget(latitude_line)
        latitude_layout.addWidget(north_checkbox)
        latitude_layout.addWidget(south_checkbox)

        longitude_button_group = QButtonGroup()
        longitude_layout = QHBoxLayout()
        longitude_line = CoordinateLine()
        east_checkbox = CoordinateRadioButton("East")
        west_checkbox = CoordinateRadioButton("West")
        longitude_button_group.addButton(east_checkbox)
        longitude_button_group.addButton(west_checkbox)
        longitude_layout.addWidget(longitude_line)
        longitude_layout.addWidget(east_checkbox)
        longitude_layout.addWidget(west_checkbox)

        longitude_line.setText("0.00")
        latitude_line.setText("0.00")
        north_checkbox.setChecked(1)
        east_checkbox.setChecked(1)

        longitude_line.textChanged.connect(self.update_coordinates_label)
        latitude_line.textChanged.connect(self.update_coordinates_label)
        west_checkbox.toggled.connect(self.update_coordinates_label)
        south_checkbox.toggled.connect(self.update_coordinates_label)

        coordinates_rounded_label = QLabel()
        show_map_button = QPushButton("Show location on map")
        show_map_button.setCheckable(True)
        show_map_button.clicked.connect(self.show_map)

        download_forecast_button = QPushButton("Download")
        show_forecast_button = QPushButton("Show")
        button_layout = QHBoxLayout()

        button_layout.addWidget(download_forecast_button)
        button_layout.addWidget(show_forecast_button )

        layout.addWidget(QLabel("Latitude:"))
        layout.addLayout(latitude_layout)
        layout.addWidget(QLabel("Longitude:"))
        layout.addLayout(longitude_layout)
        layout.addWidget(coordinates_rounded_label)
        layout.addWidget(show_map_button)
        layout.addWidget(forecast_date_picker)
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.latitude = 0
        self.longitude = 0
        self.latitude_round = 0
        self.longitude_round = 0

    def show_map(self):
        # From GeoPandas, our world map data
        worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        # Creating axes and plotting world map
        fig, ax = plt.subplots(figsize=(10, 5))
        worldmap.plot(color="lightgrey", ax=ax)
        plt.scatter(self.longitude, self.latitude)
        plt.scatter(self.longitude_round, self.latitude_round)
        plt.show()

    def update_coordinates_label(self):
        self.latitude = self.latitude_line.text()
        self.longitude = self.longitude_line.text()

        try:
            self.latitude = float(self.latitude)
            self.longitude = float(self.longitude)
            self.latitude_round = round_coordinates(float(self.latitude))
            self.longitude_round = round_coordinates(float(self.longitude))
        except Exception:
            QMessageBox.about(self, 'Error', 'Input a number with a dot!')



        if self.south_checkbox.isChecked():
            self.latitude_round = -self.latitude_round
            self.latitude = - self.latitude
        if self.west_checkbox.isChecked():
            self.longitude_round = -self.longitude_round
            self.longitude = - self.longitude

        self.coordinates_rounded_label.setText('Current coordinates: ' + str(self.latitude_round) + ' ' + str(self.longitude_round))


