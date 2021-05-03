from datetime import datetime

from jinja2 import Template
from sunnyday import Weather


class ForecastPrettifier:

    __DT_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, weather: Weather):
        self.weather = weather
        self.prettified = [{'dt': datetime.strptime(forecast['dt_txt'], self.__DT_FORMAT),
                            'temp': forecast['main']['temp'],
                            'desc': forecast['weather'][0]['description'],
                            'icon': forecast['weather'][0]['icon']}
                           for forecast in weather.next_12h()]


class Jinja2Processor:

    class HtmlError(OSError):
        pass

    def __init__(self, path: str, **kwargs):
        self.template = Template(self._get_html(path))
        self.content = self.template.render(**kwargs)

    @classmethod
    def _get_html(cls, path: str) -> str:
        try:
            with open(path) as html:
                return html.read()
        except OSError as e:
            raise cls.HtmlError(e.strerror) from None
