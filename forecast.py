from pathlib import Path

from folium import Map

from geo import GeoPoint, GeoMarker

LOCATIONS = [[41, -1], [40, 2], [50, 113], [-20, -70]]
POPUP = str(Path.cwd() / 'popup.html')
MAP = Map()

for lat, lon in LOCATIONS:
    geo = GeoPoint(lat, lon)
    marker = GeoMarker(geo, POPUP)
    marker.mark(MAP)

MAP.save('map.html')
