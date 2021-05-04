from datetime import datetime
from typing import Optional

from folium import Marker, Popup, Map
from pytz import timezone
from sunnyday import Weather
from timezonefinder import TimezoneFinder

from .util import Jinja2Processor, ForecastPrettifier


class GeoPoint:

    __API_KEY = '6e4fdb0fbf72689037ddd1d49b02d537'

    def __init__(self, latitude: int, longitude: int):
        self.latitude = latitude
        self.longitude = longitude

    def get_time(self) -> Optional[datetime]:
        tz_str = TimezoneFinder().timezone_at(lng=self.longitude, lat=self.latitude)
        if not tz_str:
            return None
        tz = timezone(tz_str)
        tz_now = datetime.now(tz=tz)
        return tz_now

    def get_weather(self) -> list:
        weather = Weather(apikey=self.__API_KEY, lat=self.latitude, lon=self.longitude)
        return ForecastPrettifier(weather).prettified


class GeoMarker:

    def __init__(self, geo: GeoPoint, popup_path: str, *args, **kwargs):
        self.geo = geo
        weather = Jinja2Processor(popup_path, casts=geo.get_weather()).content
        self.marker = Marker(location=[self.geo.latitude, self.geo.longitude],
                             popup=Popup(weather),
                             *args, **kwargs)

    def mark(self, map_: Map) -> None:
        self.marker.add_to(map_)
