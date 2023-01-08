import netCDF4
from netCDF4 import date2index
from datetime import datetime, timezone, timedelta
from utility import *

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

        self.times = None
        self.lats = None
        self.lons = None
        self.vwinds = None
        self.uwinds = None
        self.pressures = None
        self.temperatures = None

        self.download_latest_forecast()
        self.set_latitude(latitude)
        self.set_longitude(longitude)

    def download_latest_forecast(self):
        success = False
        self.forecast_file_date = datetime.now(timezone.utc)

        attempt_count = 0

        while not success and attempt_count < 10:
            attempt_count += 1
            self.forecast_file_date -= timedelta(hours=6 * attempt_count)
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
                print("Dataset ", self.gfs_url, "not found!")

            else:
                print("Dataset found!")
                success = True

    def process_gfs_forecast(self):
        time = self.gfs_dataset.variables["time"]
        uwind = self.gfs_dataset.variables["ugrdprs"]
        vwind = self.gfs_dataset.variables["vgrdprs"]
        surface_geopotential_height = self.gfs_dataset.variables["hgtsfc"]
        geopotential_heights = self.gfs_dataset.variables["hgtprs"]
        temperatures = self.gfs_dataset.variables["hgtprs"]
        pressures = self.gfs_dataset.variables["hgtprs"]
        lats = self.gfs_dataset.variables["lat"][:].tolist()
        lons = self.gfs_dataset.variables["lon"][:].tolist()

        forecast_day_index = date2index(self.forecast_datetime, time, calendar="gregorian")
        print("Time index: ", forecast_day_index)
        print("Latitude index ", lats.index(50))
        print(time[forecast_day_index])
        print(time[forecast_day_index]-time[0])
        print(time[1])
        print(time[3])
        print(uwind[0,0,0,0])
        print(lats[0])
        print('pause')

    def set_latitude(self, latitude):
        self.latitude = latitude
        self.latitude_index = se

    def set_longitude(self, longitude):
        pass

    def get_wind_profile(self, date, latitude, longitude):
        pass


def find_lat_index(latitude):
    """
    Finds the index of the nearest latitude point in a latitude list in a netcfd4 file with GFS forecast
    :param latitude: float number representing latitude
    :return:
    """

    latitude_round = round_coordinates(latitude)


def find_lon_index(longitude):

    longitude_round = round_coordinates(longitude)
    pass




