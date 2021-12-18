#!/usr/bin/env python3

import argparse
import re
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto
from datetime import datetime, timedelta
import urllib.request
import json
import config as cfg
import math

days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

def drawSun():
    for x in range(weatherLeft, weatherRight):
        for y in range(weatherTop, weatherBottom):
            if math.sqrt((x - weatherCenter[0])**2 + (y - weatherCenter[1])**2) < r:
                img.putpixel((x, y), inky_display.RED)

# def getHeadlines():

def getWeather():
    forecast = ""
    latlong = cfg.latlong
    
    pointsApiJson = urllib.request.urlopen("https://api.weather.gov/points/" + latlong).read()
    pointsApiDict = json.loads(pointsApiJson)
    
    forecastApi = pointsApiDict["properties"]["forecast"]
    forecastApiJson = urllib.request.urlopen(forecastApi).read()
    forecastApiDict = json.loads(forecastApiJson)
    forecastTime = forecastApiDict["properties"]["updated"]
    forecasts = forecastApiDict["properties"]["periods"]

    for i in forecasts:
        forecast = forecast + i["name"] + " - " + str(i["temperature"]) + i["temperatureUnit"] + " - " + i["shortForecast"] + "\n"
    return forecast

def getHeadlines():
    headlinestr = ''
    api = cfg.apikey

    if not api:
        print("Need NYT API key")
        exit()

    apiJson = urllib.request.urlopen("https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=" + api).read()
    decode = apiJson.decode('utf-8')
    apiDict = json.loads(decode)

    i = 0
    for article in apiDict["results"]:
        i = i + 1
        if i > 3: 
            continue
        headlinestr = headlinestr + article["title"] + "\n"
        headlinestr = headlinestr + article["abstract"] + "\n"
    return headlinestr

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

parser = argparse.ArgumentParser()
# parser.add_argument('--name', '-n', type=str, required=True, help="Your name")
args, _ = parser.parse_known_args()

# inky_display.set_rotation(180)
try:
    inky_display.set_border(inky_display.RED)
except NotImplementedError:
    pass

# Figure out scaling for display size

scale_size = 1.0
padding = 0

if inky_display.resolution == (400, 300):
    scale_size = 2.20
    padding = 15

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30

if inky_display.resolution == (250, 122):
    scale_size = 1.30
    padding = -5

# Create a new canvas to draw on

img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

# Load the fonts

intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(16 * scale_size))
ebeFont = ImageFont.truetype(font='./ebe.ttf', size=int(10 * scale_size))
teleFont = ImageFont.truetype(font='./tele.ttf', size=int(10 * scale_size))
dateFont = ImageFont.truetype(font='./tele.ttf', size=int(18 * scale_size))
timeFont = ImageFont.truetype(font='./tele.ttf', size=int(48 * scale_size))

# Grab the name to be displayed

# name = args.name

# borders

# weather-box

# weatherTop = 0
# weatherBottom = int(inky_display.height * .4)
# weatherLeft = int(inky_display.width - (inky_display.width * .3))
# weatherRight = int(inky_display.width)
# weatherCenter = [int((weatherLeft + weatherRight)/2),int((weatherBottom + weatherTop)/2)]
# r = 20

# for y in range(weatherTop, weatherBottom):
    # img.putpixel((weatherLeft,y), inky_display.BLACK)
# for x in range(weatherLeft, weatherRight):
    # img.putpixel((x,weatherBottom), inky_display.BLACK)

forecast = getWeather()
toShow = forecast.split('\n')[0:3]

font = teleFont
totalH = 0
totalW = 0
maxDayW = 0
maxTempW = 0
for i in toShow:
    w, h = font.getsize(i)
    totalH = totalH + h
    totalW = totalW + w
    for j, val in enumerate(i.split(' - ')):
        if j == 0:
            val = re.sub('This ', '', val)
        vw, vh = font.getsize(val)
        if j == 0 and vw > maxDayW:
            maxDayW = vw
        elif j == 1 and vw > maxTempW:
            maxTempW = vw

print("totalW: " + str(totalW) + ", totalH: " + str(totalH))
line = inky_display.height
wpadding = 10
for i in reversed(toShow):
    w, h = font.getsize(i)
    line = line - h
    for j, val in enumerate(i.split(' - ')):
        x = 0
        if j == 0: # time
            val = re.sub('This ', '', val)
            x = 0
        elif j == 1: # temp
            x = maxDayW + wpadding
        elif j == 2: # forecast
            x = maxDayW + wpadding + maxTempW + wpadding
        draw.text((x, line), val, inky_display.BLACK, font=font)

# date-time

now = datetime.now()
now = now - timedelta(hours=-7)
time = now.strftime("%H:%M")
date = now.strftime("%m/%d/%Y")
day = days[now.weekday()]
vPadding = 2

draw.text((0,vPadding), time, inky_display.BLACK, font=timeFont)
timew, timeh = timeFont.getsize(time)
draw.text((0,timeh + vPadding), day + " " + date, inky_display.BLACK, font=dateFont)
datew, dateh = dateFont.getsize(day + " " + date)

# headlines

headlines = getHeadlines()
for i,headline in enumerate(headlines.split('\n')):
	headlinew, headlineh, = font.getsize(headline)
	draw.text((0, vPadding + timeh + vPadding + dateh + vPadding + ((vPadding + headlineh) * i)), headline, inky_display.BLACK, font=font)

# Draw the red, white, and red strips

# for y in range(0, y_top):
    # for x in range(0, inky_display.width):
        # img.putpixel((x, y), inky_display.BLACK if inky_display.colour == "black" else inky_display.RED)

# for y in range(y_top, y_bottom):
    # for x in range(0, inky_display.width):
        # img.putpixel((x, y), inky_display.WHITE)

# for y in range(y_bottom, inky_display.height):
    # for x in range(0, inky_display.width):
        # img.putpixel((x, y), inky_display.BLACK if inky_display.colour == "black" else inky_display.RED)

# Calculate the positioning and draw the "Hello" text

# hello_w, hello_h = hanken_bold_font.getsize("Hello")
# hello_x = int((inky_display.width - hello_w) / 2)
# hello_y = 0 + padding
# draw.text((hello_x, hello_y), "Hello", inky_display.WHITE, font=hanken_bold_font)

# Calculate the positioning and draw the "my name is" text

# mynameis_w, mynameis_h = hanken_medium_font.getsize("my name is")
# mynameis_x = int((inky_display.width - mynameis_w) / 2)
# mynameis_y = hello_h + padding
# draw.text((mynameis_x, mynameis_y), "my name is", inky_display.WHITE, font=hanken_medium_font)

# Calculate the positioning and draw the name text

# name_w, name_h = intuitive_font.getsize(name)
# name_x = int((inky_display.width - name_w) / 2)
# name_y = int(y_top + ((y_bottom - y_top - name_h) / 2))
# draw.text((name_x, name_y), name, inky_display.BLACK, font=intuitive_font)

# Display the completed name badge

inky_display.set_image(img)
inky_display.show()
