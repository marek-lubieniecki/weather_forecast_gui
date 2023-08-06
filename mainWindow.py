import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QDateEdit, QVBoxLayout, QHBoxLayout, QGridLayout,QButtonGroup, \
    QLineEdit, QLabel, QWidget, QPushButton, QMessageBox, QComboBox, QSpinBox, QFileDialog, QProgressDialog
from PyQt5.QtCore import QObject, pyqtSignal, Qt

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

from threading import Thread

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
        self.hours = [3 * x for x in range(0, 7)]
        self.environment = None
        self.forecast = None

        self.signals()
        self.ui_components()
        self.load_forecast()
        self.update_coordinates_label()

    def signals(self):
        self.message_obj = Message()

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
        self.download_forecast_button = QPushButton("Save as")
        self.download_forecast_button.clicked.connect(self.save_forecast)
        self.button_layout = QHBoxLayout(self)

        self.show_forecast_button.clicked.connect(self.show_btn_clicked)
        self.datetime_layout = QHBoxLayout(self)
        self.datetime_layout.addWidget(self.forecast_number)
        self.datetime_layout.addWidget(self.forecast_date)
        self.datetime_layout.addWidget(self.forecast_hour)

        self.button_layout.addWidget(self.show_forecast_button)
        self.button_layout.addWidget(self.download_forecast_button)

        self.forecast_data_label = QLabel()

        self.sc = MplCanvas(self, width=8, height=7, dpi=100)
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
        self.main_left_layout.addWidget(self.forecast_data_label)
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
        self.forecast_data_label.setText("Current forecast loaded" + "\n" + str(self.forecast.gfs_url))

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

    def set_forecast_location(self):
        self.forecast.load_forecast_for_coordinates(self.latitude_round, self.longitude_round)

    def show_btn_clicked(self):
        self.progress_indicator = QProgressDialog(self)
        self.progress_indicator.setWindowModality(Qt.WindowModal)
        self.progress_indicator.setRange(0, 0)
        self.progress_indicator.setAttribute(Qt.WA_DeleteOnClose)
        self.progress_indicator.setWindowTitle("GFS GUI")
        self.progress_indicator.setLabelText("Downloading forecast")
        self.progress_indicator.setCancelButton(None)
        self.message_obj.finished.connect(self.progress_indicator.close, Qt.QueuedConnection)
        self.progress_indicator.show()

        x = Thread(target=self.plot_wind_profile, args=[self.message_obj])
        x.start()

    def plot_wind_profile(self, obj):

        date = self.forecast_date.date()
        pydate = date.toPyDate()
        hour = int(self.forecast_hour.currentText())
        forecast_date = datetime(pydate.year, pydate.month, pydate.day, hour)
        self.forecast.get_wind_profile(forecast_date, self.latitude_round, self.longitude_round)
        self.forecast_number.setValue(self.forecast.date_index)
        self.sc.plot_ax1(self.forecast.wind_speed_profile, self.forecast.heights_profile)
        self.sc.plot_ax2(self.forecast.wind_heading_profile, self.forecast.heights_profile)
        self.sc.update_plot()
        obj.finished.emit()

    def save_forecast(self):
        file_name = QFileDialog.getSaveFileName(self, "Save File", 'forecast.txt', '.txt')
        if file_name:
            numpy.savetxt(file_name[0], self.forecast.forecast_array, delimiter=',')


class Message(QObject):
    finished = pyqtSignal()


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.tight_layout()
        self.ax1 = self.fig.subplots(nrows=1)
        self.ax2 = self.ax1.twiny()

        self.format_plot()
        super(MplCanvas, self).__init__(self.fig)


    def format_plot(self):
        self.ax1.set_xlabel("Wind speed [m/s]", color="blue")
        self.ax2.set_xlabel("Wind heading [deg]", color="red")

        self.ax1.set_ylabel("Altitude [m]")
        self.ax1.grid()
        self.ax1.set_xlim([0, 60])
        self.ax2.set_xlim([0, 360])
        self.ax2.set_xticks(np.linspace(0, 360, 7))
        self.ax2.spines["bottom"].set_color("blue")
        self.ax2.spines["top"].set_color("red")

        self.fig.set_figheight(6)
        self.fig.set_figwidth(6)

    def update_plot(self):
        self.format_plot()
        self.draw()

    def plot_ax1(self, x, y):
        self.ax1.clear()  # Clear the canvas.
        self.ax1.plot(x, y, color='blue')

    def plot_ax2(self, x, y):
        self.ax2.clear()  # Clear the canvas.
        self.ax2.plot(x, y, color='red')
