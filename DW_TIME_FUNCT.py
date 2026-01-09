import os
import time
from time import gmtime, strftime
import zoneinfo
from datetime import datetime

def time_grab():
    os.environ['TZ'] = 'US/Eastern'
    time.tzset()
    time.tzname
    eastern_now = datetime.now(zoneinfo.ZoneInfo("America/New_York"))
    # Month, Day, Year, Hour, Minute, Second
    mo = eastern_now.month
    da = eastern_now.day
    ye = eastern_now.year
    ho = eastern_now.hour
    mi = eastern_now.minute
    se = eastern_now.second
    return mo, da, ye, ho, mi, se
