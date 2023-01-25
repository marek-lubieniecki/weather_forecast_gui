import math

import netCDF4
import numpy as np
from netCDF4 import date2index
from datetime import datetime, timezone, timedelta
from utility import *
import time
import xarray

class GfsForecast:
    def __init__(self, latitude, longitude, forecast_datetime, forecast_interval):
        self.latitude = latitude
        self.longitude = longitude
        self.forecast_datetime = forecast_datetime
        self.forecast_interval = forecast_interval
        self.date_today = datetime.today()

        self.gfs_url = ''
        self.gfs_dataset = None
        self.forecast_file_date = None

        self.latitude_index = 0
        self.longitude_index = 0
        self.date_index = 0

        self.times = None
        self.lats = None
        self.lons = None
        self.vwinds = None
        self.uwinds = None
        self.pressures = None
        self.temperatures = None
        self.surface_geopotential_height = None
        self.geopotential_heights = None

        self.heights_profile = None
        self.vwinds_profile = None
        self.uwinds_profile = None
        self.temperature_profile = None
        self.pressure_profile = None

        self.wind_speed_profile = None
        self.wind_heading_profile = None


        self.uwinds_array = None
        self.vwinds_array = None
        self.times_array = None

        self.number_of_forecast_points = 0
        self.number_of_altitude_points = 0

        self.download_latest_forecast()
        self.load_forecast_variables()
        self.set_latitude(latitude)
        self.set_longitude(longitude)


    def download_latest_forecast(self):
        success = False
        self.forecast_file_date = datetime.now(timezone.utc)

        attempt_count = 0

        while not success and attempt_count < 10:
            attempt_count += 1
            self.forecast_file_date -= timedelta(hours=6)
            hour_round = 6 * (self.forecast_file_date.hour // 6)
            self.forecast_file_date = self.forecast_file_date.replace(hour=hour_round, minute=0, second=0,
                                                                      microsecond=0)

            self.gfs_url = "https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{:04d}{:02d}{:02d}/gfs_0p25_{:02d}z".format(
                self.forecast_file_date.year,
                self.forecast_file_date.month,
                self.forecast_file_date.day,
                self.forecast_file_date.hour)

            try:
                print("Retrieving file: ", str(self.forecast_file_date))
                print("GFS Url: ", self.gfs_url)
                self.gfs_dataset = netCDF4.Dataset(self.gfs_url)

            except OSError:
                print("\nDataset ", self.gfs_url, "not found!")

            else:
                print("\nDataset found!")
                success = True

    def load_forecast_variables(self):
        self.times = self.gfs_dataset.variables["time"]
        self.lats = self.gfs_dataset.variables["lat"][:].tolist()
        self.lons = self.gfs_dataset.variables["lon"][:].tolist()
        self.uwinds = self.gfs_dataset.variables["ugrdprs"]
        self.vwinds = self.gfs_dataset.variables["vgrdprs"]
        self.temperatures = self.gfs_dataset.variables["hgtprs"]
        self.pressures = self.gfs_dataset.variables["hgtprs"]
        self.surface_geopotential_height = self.gfs_dataset.variables["hgtsfc"]
        self.geopotential_heights = self.gfs_dataset.variables["hgtprs"]

        self.number_of_forecast_points = self.times.size
        self.number_of_altitude_points = self.geopotential_heights.shape[1]

    def set_datetime(self, forecast_datetime):
        self.forecast_datetime = forecast_datetime
        self.date_index = date2index(self.forecast_datetime, self.times, calendar="gregorian")

    def set_latitude(self, latitude):
        self.latitude = round_to_quarter(latitude)
        self.latitude_index = self.lats.index(self.latitude)

    def set_longitude(self, longitude):
        self.longitude = round_to_quarter(longitude)
        self.longitude_index = self.lons.index(self.longitude)

    def load_forecast_for_coordinates(self, latitude, longitude):


        time_slice = (0, 10)

        test_dataset = xarray.open_dataset(self.gfs_url)
        var = ['ugrdprs']
        st = time.time()
        test_dataset[var].isel(time=slice(*time_slice)).sel(lat=self.latitude, lon=self.longitude).to_netcdf('test_uwind.nc')
        et = time.time()
        elapsed_time = et - st
        print('Var saved in', elapsed_time)
        #test_dataset_2 = xarray.open_dataset('test_uwind.nc')
        #print("Var opened")
        self.set_latitude(latitude)
        self.set_longitude(longitude)

        self.uwinds_array = np.zeros((self.number_of_forecast_points, self.number_of_altitude_points))
        self.vwinds_array = np.zeros((self.number_of_forecast_points, self.number_of_altitude_points))

        for i in range(5):
                st = time.time()
                self.uwinds_array[i][:] = self.uwinds[i, :, self.latitude_index, self.longitude_index]
                self.vwinds_array[i][:] = self.uwinds[i, :, self.latitude_index, self.longitude_index]
                et = time.time()
                elapsed_time = et - st
                print(i, ' ', elapsed_time)

        print("Loading complete")

    def get_wind_profile(self, forecast_datetime, latitude, longitude):

        self.set_latitude(latitude)
        self.set_longitude(longitude)
        self.set_datetime(forecast_datetime)

        self.uwinds_profile = self.uwinds[self.date_index, :, self.latitude_index, self.longitude_index]
        self.vwinds_profile = self.vwinds[self.date_index, :, self.latitude_index, self.longitude_index]
        self.heights_profile = self.geopotential_heights[self.date_index, :, self.latitude_index, self.longitude_index]
        self.temperature_profile = self.temperatures[self.date_index, :, self.latitude_index, self.longitude_index]

        self.wind_speed_profile = []

        for i in range(self.number_of_altitude_points):
            wind_speed = math.sqrt(self.uwinds_profile[i]*self.uwinds_profile[i] + self.vwinds_profile[i]*self.vwinds_profile[i])
            self.wind_speed_profile.append(wind_speed)



