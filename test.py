from GfsForecast import *
from datetime import datetime


today = datetime.today()
latitude = 54.569003
longitude = 16.717153

date = datetime(year=2023, month=1, day=11, hour=12)

test_forecast = GfsForecast(latitude=latitude, longitude=longitude, forecast_datetime=date, forecast_interval=1)
test_forecast.download_latest_forecast()
test_forecast.process_gfs_forecast()