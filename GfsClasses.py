
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

