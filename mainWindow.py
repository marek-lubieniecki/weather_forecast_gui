import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDateEdit, QVBoxLayout, QHBoxLayout, QGridLayout,QButtonGroup, \
    QLineEdit, QLabel, QWidget, QPushButton, QMessageBox, QComboBox


from widgetConfig import *
from utility import *
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime
from rocketpy import Environment

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GFS GUI")

        self.latitude = 0
        self.longitude = 0
        self.latitude_round = 0
        self.longitude_round = 0
        self.date = None
        self.hour = None
        self.hours = list(range(24))
        self.environment = None

        self.UiComponents()


    def UiComponents(self):
        layout = QVBoxLayout()
        coordinate_layout = QHBoxLayout()
        central_widget = QWidget()

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
        self.west_checkbox.toggled.connect(self.update_coordinates_label)
        self.south_checkbox.toggled.connect(self.update_coordinates_label)

        self.coordinates_rounded_label = QLabel()
        self.show_map_button = QPushButton("Show location on map")
        self.show_map_button.setCheckable(True)
        self.show_map_button.clicked.connect(self.show_map)

        self.forecast_date = QDateEdit(datetime.today())
        self.forecast_hour = QComboBox()
        for hour in self.hours: self.forecast_hour.addItem(str(hour))
        self.forecast_hour.setCurrentText("12")

        self.show_forecast_button = QPushButton("Show")
        self.download_forecast_button = QPushButton("Save")
        self.button_layout = QHBoxLayout(self)

        self.show_forecast_button.clicked.connect(self.set_forecast)

        self.button_layout.addWidget(self.show_forecast_button)
        self.button_layout.addWidget(self.download_forecast_button)

        self.datetime_layout = QHBoxLayout(self)
        self.datetime_layout.addWidget(self.forecast_date)
        self.datetime_layout.addWidget(self.forecast_hour)

        layout.addWidget(QLabel("Latitude:"))
        layout.addLayout(self.latitude_layout)
        layout.addWidget(QLabel("Longitude:"))
        layout.addLayout(self.longitude_layout)
        layout.addWidget(self.coordinates_rounded_label)
        layout.addWidget(self.show_map_button)
        layout.addLayout(self.datetime_layout)
        layout.addLayout(self.button_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



    def show_map(self):
        # From GeoPandas, our world map data
        worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        # Creating axes and plotting world map
        fig, ax = plt.subplots(figsize=(12, 6))
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
            self.latitude_round = round_coordinates(self.latitude)
            self.longitude_round = round_coordinates(self.longitude)

        except ValueError:
            QMessageBox.about(self, 'Error', 'Input a number')

        if self.south_checkbox.isChecked():
            self.latitude_round = -self.latitude_round
            self.latitude = - self.latitude
        if self.west_checkbox.isChecked():
            self.longitude_round = -self.longitude_round
            self.longitude = - self.longitude

        self.coordinates_rounded_label.setText('Current coordinates: ' + str(self.latitude_round) + ' ' + str(self.longitude_round))

    def set_forecast(self):

        date = self.forecast_date.date()
        year = date.year()
        month = date.month()
        day = date.day()
        hour = int(self.forecast_hour.currentText())
        print(year, month, day, hour)
        self.environment = Environment(railLength=0,
                                       latitude=self.latitude_round,
                                       longitude=self.longitude_round,
                                       elevation=0,
                                       date=(year, month, day, hour))

        self.environment.setAtmosphericModel(type='Forecast', file='GFS')
        self.environment.allInfo()

    def save_forecast(self):
        pass