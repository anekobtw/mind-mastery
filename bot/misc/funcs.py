import os
import time
from datetime import datetime, timedelta, timezone

import pytz
from aiogram import types
from dateutil import parser, tz
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from database import SettingsManager

geolocator = Nominatim(user_agent="anekobtw")
tzfinder = TimezoneFinder()


def get_tz_text(*, location: str = None, approximate_time: str = None) -> tuple[tuple[str], int]:
    # getting timezone and offset
    if location:
        user_timezone, offset_secs = get_utcoffset_from_location(location)
    elif approximate_time:
        user_timezone, offset_secs = get_utcoffset_from_time(approximate_time)

    # getting offset
    sign = "+" if offset_secs > 0 else ""

    return (
        f"Your time zone: <b>UTC{sign}{round(offset_secs / 3600, 1)}</b>\n",
        f'Your local time: <b>{datetime.now(tz=user_timezone).strftime("%d %b %Y %H:%M:%S")}</b>\n\n',
        "If that is correct, please press ✅ button. Otherwise, press ❌ button\n",
        "If you don't press anything, this time zone will be used.",
    ), offset_secs


def get_utcoffset_from_location(location: str) -> tuple[str, int]:
    loc = geolocator.geocode(location)
    time.sleep(1)  # in order not to get a ban
    user_tz = tz.gettz(tzfinder.timezone_at(lng=loc.longitude, lat=loc.latitude))
    return user_tz, int(user_tz.utcoffset(datetime.now()).total_seconds())


def get_utcoffset_from_time(approximate_time: str):
    result = ["city_name", 99999]
    splitted = approximate_time.split(":")
    local_time_seconds = int(splitted[0]) * 60 + int(splitted[1])

    for time_zone in pytz.all_timezones:
        timezone_datetime = datetime.now(tz=pytz.timezone(time_zone))
        timezone_time_seconds = timezone_datetime.hour * 60 + timezone_datetime.minute
        if abs(local_time_seconds - timezone_time_seconds) <= result[1]:
            result[0] = time_zone
            result[1] = abs(local_time_seconds - timezone_time_seconds)

    return pytz.timezone(result[0]), int(pytz.timezone(result[0]).utcoffset(datetime.now()).total_seconds())


def get_utc_timestamp() -> int:
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    return int(utc_time.timestamp())


def local_to_utc(message: types.Message, with_interval: bool) -> tuple[int, int]:
    load_dotenv()
    my_timezone_seconds = int(os.getenv("MY_TIMEZONE_AHEAD_SECONDS"))
    user_timezone_seconds = SettingsManager().get_user_settings(message.from_user.id)[1]
    if with_interval:
        hour, minute = map(int, message.text.split(":"))
        time = datetime(2000, 1, 1, hour, minute, 0) + timedelta(seconds=my_timezone_seconds) - timedelta(seconds=user_timezone_seconds)
        return time.hour, time.minute
    else:
        local_datetime = parser.parse(message.text, fuzzy=True)
        adjusted_datetime = local_datetime + timedelta(seconds=my_timezone_seconds) - timedelta(seconds=user_timezone_seconds)
        return local_datetime, adjusted_datetime


def utc_to_local(user_id: int, with_interval: bool, *, hour: int = None, minute: int = None, timestamp: int = None) -> datetime:
    load_dotenv()
    my_timezone_seconds = int(os.getenv("MY_TIMEZONE_AHEAD_SECONDS"))
    user_timezone_seconds = SettingsManager().get_user_settings(user_id)[1]
    if with_interval:
        return datetime(2000, 1, 1, hour, minute, 0) - timedelta(seconds=my_timezone_seconds) + timedelta(seconds=user_timezone_seconds)
    else:
        return datetime.fromtimestamp(timestamp) - timedelta(seconds=my_timezone_seconds) + timedelta(seconds=user_timezone_seconds)
