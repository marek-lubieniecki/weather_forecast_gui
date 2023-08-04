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
        self.forecast_array = None

        self.number_of_forecast_points = 0
        self.number_of_altitude_points = 0

        self.download_latest_forecast()
        self.load_forecast_variables()
        #self.set_latitude(latitude)
        #self.set_longitude(longitude)

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

            self.gfs_url = "http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs{:04d}{:02d}{:02d}/gfs_0p25" \
                           "_{:02d}z".format(
                self.forecast_file_date.year,
                self.forecast_file_date.month,
                self.forecast_file_date.day,
                self.forecast_file_date.hour)

            try:
                print("Retrieving file: ", str(self.forecast_file_date))
                print("GFS Url: ", self.gfs_url)
                self.gfs_dataset_xarray = xarray.open_dataset(self.gfs_url)
                print("Xarray opened!")
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
        self.temperatures = self.gfs_dataset.variables["tmpprs"]
        self.pressures = self.gfs_dataset.variables["lev"][:].tolist()
        self.surface_geopotential_height = self.gfs_dataset.variables["hgtsfc"]
        self.geopotential_heights = self.gfs_dataset.variables["hgtprs"]

        self.number_of_forecast_points = self.times.size
        self.number_of_altitude_points = self.geopotential_heights.shape[1]
        self.forecast_array = np.zeros((self.number_of_altitude_points, 5))

    def set_datetime(self, forecast_datetime):
        self.forecast_datetime = forecast_datetime
        self.date_index = date2index(self.forecast_datetime, self.times, calendar="gregorian")
        print("Date index set to :", self.date_index)

    def set_latitude(self, latitude):
        self.latitude = round_to_quarter(latitude)
        self.latitude_index = self.lats.index(self.latitude)
        print("Latitude index set to :", self.latitude_index )

    def set_longitude(self, longitude):
        if longitude < 0:
            longitude = 360 + longitude
        self.longitude = round_to_quarter(longitude)
        self.longitude_index = self.lons.index(self.longitude)
        print("Longitude index set to :", self.longitude_index)

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
        self.wind_heading_profile = []

        for i in range(self.number_of_altitude_points):
            altitude = self.heights_profile[i]
            u = self.uwinds_profile[i]
            v = self.vwinds_profile[i]
            temperature = self.temperature_profile[i]
            pressure = self.pressures[i]

            self.forecast_array[i][0] = altitude
            self.forecast_array[i][1] = u
            self.forecast_array[i][2] = v
            self.forecast_array[i][3] = temperature
            self.forecast_array[i][4] = pressure

            wind_speed = math.sqrt(u*u + v*v)
            wind_heading = (math.degrees(math.atan2(v, u)))
            if wind_heading < 0:
                wind_heading = wind_heading + 360

            self.wind_speed_profile.append(wind_speed)
            self.wind_heading_profile.append(wind_heading)


    def download_day_forecast(self, date):
        pass
        # open dataset

        # choose data for given date

        # save data to file

    def load_day_forecast(self, date):
        pass
        #check if file exists

        #try to open file

        #if not, download file


