#!/usr/bin/env python3

import urllib.request
import json
import config as cfg

latlong = cfg.latlong

pointsApiJson = urllib.request.urlopen("https://api.weather.gov/points/" + latlong).read()
pointsApiDict = json.loads(pointsApiJson)

forecastApi = pointsApiDict["properties"]["forecast"]
forecastApiJson = urllib.request.urlopen(forecastApi).read()
forecastApiDict = json.loads(forecastApiJson)
forecastTime = forecastApiDict["properties"]["updated"]
forecasts = forecastApiDict["properties"]["periods"]

for i in forecasts:
    print(i["name"] + " - " + str(i["temperature"]) + i["temperatureUnit"] + " - " + i["shortForecast"])



