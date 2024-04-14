import time
from datetime import datetime, timedelta

import pytz
from dateutil import parser, tz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

geolocator = Nominatim(user_agent="anekobtw")
tzfinder = TimezoneFinder()


def get_tz_text(*, location: str = None, approximate_time: str = None) -> tuple[tuple[str], str]:
    # getting timezone
    if location:
        loc = geolocator.geocode(location)
        time.sleep(1)  # in order not to get a ban
        timezone = tz.gettz(tzfinder.timezone_at(lng=loc.longitude, lat=loc.latitude))

    if approximate_time:
        timezone = get_timezone_from_time(approximate_time)

    # getting offset
    offset = get_timezone_offset(timezone)

    return (
        f"Your time zone: <b>GMT{offset}</b>\n",
        f'Your local time: <b>{datetime.now(tz=timezone).strftime("%d %b %Y %H:%M:%S")}</b>\n\n',
        "If that is correct, please press ✅ button. Otherwise, press ❌ button\n",
        "If you don't press anything, this time zone will be used.",
    ), offset


def get_timezone_from_time(approximate_time: str) -> str | None:
    time_zones = pytz.all_timezones
    for time_zone in time_zones:
        local_time = datetime.now(tz=pytz.timezone(time_zone))
        if local_time.strftime("%H:%M") == approximate_time:
            return time_zone
    return None


def get_timezone_offset(timezone) -> str:
    # Get UTC offset in hours and minutes
    offset = datetime.now(pytz.utc).astimezone(timezone).strftime("%z")
    offset_hours = int(offset[:-2])
    offset_minutes = int(offset[-2:])
    offset_str = f"{offset_hours:+d}"
    if offset_minutes:
        offset_str += f":{offset_minutes:02d}"
    return offset_str


def parse_datetime(input_str: str) -> datetime:
    parsed_datetime = parser.parse(input_str, fuzzy=True, tzinfos=[pytz.timezone("UTC")])
    return parsed_datetime


def datetime_to_utc_timestamp(datetime_obj: str) -> int:
    return datetime_obj.astimezone(tz.tzutc()).timestamp()
