import netCDF4
from datetime import datetime, date

class GfsForecast:
    def __init__(self, latitude, longitude, datetime, forecast_interval):
        self.latitude = latitude
        self.longitude = longitude
        self.datetime = datetime
        self.forecast_interval = forecast_interval
        self.date_today = datetime.today()
        self.gfs_url = ''

    def generate_gfs_url(self):
        pass

    def download_gfs_forecast(self):
        dataset = netCDF4.Dataset(self.gfs_url)
        uwind = dataset.variables["ugrdprs"]
        vwind = dataset.variables["vgrdprs"]
        altitudes = dataset.variables["lev"]
        lats = dataset.variables["lat"]
        lons = dataset.variables["lon"]
        time = dataset.variables["time"]


