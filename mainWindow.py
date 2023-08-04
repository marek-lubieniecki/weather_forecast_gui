import sys

import numpy
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QDateEdit, QVBoxLayout, QHBoxLayout, QGridLayout,QButtonGroup, \
    QLineEdit, QLabel, QWidget, QPushButton, QMessageBox, QComboBox, QSpinBox
from PyQt5.QtCore import Qt

from widgetConfig import *
from utility import *
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime
from rocketpy import Environment

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from GfsForecast import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GFS GUI")

        self.latitude = 54.561797
        self.longitude = 16.648350
        self.latitude_round = 0
        self.longitude_round = 0
        self.date = None
        self.hour = None
        self.hours = list(range(24))
        self.environment = None
        self.forecast = None

        self.ui_components()
        self.load_forecast()
        self.update_coordinates_label()

    def ui_components(self):
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

        self.longitude_line.setText(str(self.longitude))
        self.latitude_line.setText(str(self.latitude))
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

        self.forecast_number = QSpinBox()
        self.forecast_date = QDateEdit(datetime.today()+timedelta(days=1))
        self.forecast_hour = QComboBox()
        for hour in self.hours: self.forecast_hour.addItem(str(hour))
        self.forecast_hour.setCurrentText("12")

        self.show_forecast_button = QPushButton("Show")
        self.download_forecast_button = QPushButton("Save")
        self.download_forecast_button.clicked.connect(self.save_forecast)
        self.button_layout = QHBoxLayout(self)

        self.show_forecast_button.clicked.connect(self.plot_forecast)

        self.button_layout.addWidget(self.show_forecast_button)
        self.button_layout.addWidget(self.download_forecast_button)

        self.datetime_layout = QHBoxLayout(self)
        self.datetime_layout.addWidget(self.forecast_number)
        self.datetime_layout.addWidget(self.forecast_date)
        self.datetime_layout.addWidget(self.forecast_hour)

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.sc, self)

        self.main_layout = QHBoxLayout(self)

        self.main_left_layout = QVBoxLayout(self)
        self.main_right_layout = QVBoxLayout(self)

        self.main_left_layout.addWidget(QLabel("Latitude:"))
        self.main_left_layout.addLayout(self.latitude_layout)
        self.main_left_layout.addWidget(QLabel("Longitude:"))
        self.main_left_layout.addLayout(self.longitude_layout)
        self.main_left_layout.addWidget(self.coordinates_rounded_label)
        self.main_left_layout.addWidget(self.show_map_button)
        self.main_left_layout.addLayout(self.datetime_layout)
        self.main_left_layout.addLayout(self.button_layout)
        self.main_left_layout.addStretch()

        self.canvas_layout = QVBoxLayout()
        self.canvas_layout.addWidget(toolbar)
        self.canvas_layout.addWidget(self.sc)

        self.main_right_layout.addLayout(self.canvas_layout)

        self.main_layout.addLayout(self.main_left_layout)
        self.main_layout.addLayout(self.main_right_layout)

        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def load_forecast(self):
        self.forecast = GfsForecast(latitude=self.latitude_round, longitude=self.longitude_round, forecast_datetime=None, forecast_interval=None)

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
            self.latitude_round = round_to_quarter(self.latitude)
            self.longitude_round = round_to_quarter(self.longitude)

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

    def set_forecast_location(self):
        self.forecast.load_forecast_for_coordinates(self.latitude_round, self.longitude_round)

    def plot_forecast(self):
        date = self.forecast_date.date()
        pydate = date.toPyDate()
        hour = int(self.forecast_hour.currentText())
        forecast_date = datetime(pydate.year, pydate.month, pydate.day, hour)
        self.forecast.get_wind_profile(forecast_date, self.latitude_round, self.longitude_round)

        self.sc.ax1.cla()  # Clear the canvas.
        self.sc.ax1.plot(self.forecast.wind_speed_profile, self.forecast.heights_profile, color = 'blue')
        self.sc.ax2.plot(self.forecast.wind_heading_profile, self.forecast.heights_profile,  color = 'red')
        # Trigger the canvas to update and redraw.
        self.sc.draw()
        plt.show()

    def save_forecast(self):
        numpy.savetxt("atmosphere_forecast.csv",self.forecast.forecast_array,delimiter=',')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=12, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax1 = fig.subplots(nrows=1)
        self.ax2 = self.ax1.twiny()
        super(MplCanvas, self).__init__(fig)