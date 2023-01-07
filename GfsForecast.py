import netCDF4
from datetime import datetime, timezone, timedelta


class GfsForecast:
    def __init__(self, latitude, longitude, forecast_datetime, forecast_interval):
        self.latitude = latitude
        self.longitude = longitude
        self.forecast_datetime = forecast_datetime
        self.forecast_interval = forecast_interval
        self.date_today = datetime.today()

        self.gfs_url = ''
        self.forecast_update_times = [0, 6, 12, 18]
        self.gfs_dataset = None
        self.forecast_file_date = None

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

    def post_p

    def download_gfs_forecast(self):
        dataset = netCDF4.Dataset(self.gfs_url)
        uwind = dataset.variables["ugrdprs"]
        vwind = dataset.variables["vgrdprs"]
        altitudes = dataset.variables["lev"]
        lats = dataset.variables["lat"]
        lons = dataset.variables["lon"]
        time = dataset.variables["time"]

        import sys
        from datetime import date

        # class GfsLocationTime:
        #
        #     def __init__(self):
        #         self.latitude = 0
        #         self.longitude = 0
        #         self.forecastDateHour = datetime.today()
        #         self.GfsString = ""
        #
        #     def generateGfsString(self):
        #         # create string to aquire newest gfs forecast
        #         if len(str(dateToday.day)) == 1:
        #             dayString = "0" + str(dateToday.day)
        #         else:
        #             dayString = str(dateToday.day)
        #
        #         if len(str(dateToday.month)) == 1:
        #             monthString = "0" + str(dateToday.month)
        #         else:
        #             monthString = str(dateToday.month)
        #
        #         if len(str(hour)) == 1:
        #             hourString = "0" + str(hour)
        #         else:
        #             hourString = str(hour)
        #
        #         dateFile = datetime(dateToday.year, dateToday.month, dateToday.day, hour, 0, 0, 0)
        #         numberHours = int((datetime.timestamp(dateForecast) - datetime.timestamp(dateFile)) / 3600)
        #
        #         yearString = str(dateToday.year)
        #         dateString = yearString + monthString + dayString
        #
        #         if forecastInterval == 1:
        #             url = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs{}/gfs_0p25_1hr_{}z'.format(dateString,
        #                                                                                                    hourString)
        #         else:
        #             url = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs{}/gfs_0p25_{}z'.format(dateString, hourString)
        #             numberHours = numberHours / 3
        #
        #     def downloadForecastfile(self):

# find latest forecast file
# open forecast file
#
