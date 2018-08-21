from bs4 import BeautifulSoup
import json
import datetime
import sys
import os

# Outputs the primary weather data from a local weewx page to a JSON file
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

try:
     fileInput = open(sys.argv[1], "r")
except IndexError:
     sys.exit("[" + time + "] Error: file input target path not given.\n[" + time + "] Usage: python " + __file__ + " fileInput fileOutput")

try:
     fileResultString = sys.argv[2]
except IndexError:
    
     sys.exit("[" + time + "] Error: file output target path not given.\n[" + time + "] Usage: python " + __file__ + " fileInput fileOutput")

soup = BeautifulSoup(fileInput, 'html.parser')

weatherData = {}

mainData = soup.select("#stats_group > div table .stats_data")
superlativeData = soup.select("table")[1].select(".stats_data")
locationData = soup.select("table")[2].select(".data")

weatherData["temp"]                   = mainData[0].string
weatherData["windChill"]              = mainData[1].string
weatherData["heatIndex"]              = mainData[2].string
weatherData["dewPoint"]               = mainData[3].string
weatherData["humidity"]               = mainData[4].string
weatherData["barometer"]              = mainData[5].string
weatherData["barometerTrend"]         = mainData[6].string
weatherData["wind"]                   = mainData[7].string
weatherData["rainRate"]               = mainData[8].string
weatherData["highTemp"]               = superlativeData[0].get_text().splitlines()[1].lstrip()
weatherData["lowTemp"]                = superlativeData[0].get_text().splitlines()[2].lstrip()
weatherData["highHeatIndex"]          = superlativeData[1].get_text().splitlines()[1].lstrip()
weatherData["lowWindChill"]           = superlativeData[1].get_text().splitlines()[2].lstrip()
weatherData["highHumidity"]           = superlativeData[2].get_text().splitlines()[1].lstrip()
weatherData["lowHumidity"]            = superlativeData[2].get_text().splitlines()[2].lstrip()
weatherData["highDewPoint"]           = superlativeData[3].get_text().splitlines()[1].lstrip()
weatherData["lowDewPoint"]            = superlativeData[3].get_text().splitlines()[2].lstrip()
weatherData["highBarometer"]          = superlativeData[4].get_text().splitlines()[1].lstrip()
weatherData["lowBarometer"]           = superlativeData[4].get_text().splitlines()[2].lstrip()
weatherData["rainToday"]              = superlativeData[5].get_text()
weatherData["rainRate"]               = superlativeData[6].get_text()
weatherData["highWind"]               = superlativeData[7].get_text().splitlines()[1].lstrip()
weatherData["averageWind"]            = superlativeData[8].get_text().splitlines()[1].lstrip()
weatherData["rmsWind"]                = superlativeData[9].get_text().splitlines()[1].lstrip()
weatherData["vectorAverageSpeed"]     = superlativeData[10].get_text().splitlines()[1].lstrip()
weatherData["vectorAverageDirection"] = superlativeData[10].get_text().splitlines()[2].lstrip()
weatherData["latitude"]               = locationData[0].get_text()
weatherData["longitude"]              = locationData[1].get_text()
weatherData["altitude"]               = locationData[2].get_text()


try:
    with open(fileResultString, 'w') as fp:
        json.dump(weatherData, fp)
except Exception:
    sys.exit("[" + time + "] Error opening output file.")

print "[" + time + "] Successfully scraped data from %s and output to" % sys.argv[1], sys.argv[2] + "."
