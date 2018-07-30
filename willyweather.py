# Copyright (c) 2018 Richard Mann
# All rights reserved.
# Author: Richard Mann <mann_rj@hotmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# -----------------------------------------------------------------------
#
# WillyWeather is an Australian weather service and commercial API.
# Users must pay a per-transaction fee to access API data once 5000
# calls are reached.
#
# You must first obtain an API key from
# https://www.willyweather.com.au/info/api.html
#
# Select "Single Location" from the options.
# Select "Observational" and "Forecasts" from the sub-menu under Weather.
# This should give a $0.09 cost per 1000 requests.
#
# Enter your API key in the UI and Save, then Refresh.
# In the UI, a list of nearby stations should appear, based on your
# RainMachine latitude and longitude settings.
#
# Enter the desired Station ID in the box and save the settings.

from RMParserFramework.rmParser import RMParser
from RMUtilsFramework.rmLogging import log
from RMUtilsFramework.rmTimeUtils import *
from RMDataFramework.rmUserSettings import globalSettings

import json

class WillyWeather(RMParser):
    parserName = "WillyWeather Australia Parser"
    parserDescription = "Australian weather service from https://www.willyweather.com.au"
    parserForecast = True
    parserHistorical = False
    parserID = "willyweather"
    parserInterval = 6 * 3600
    parserEnabled = True
    parserDebug = False

    params = {
              "apiKey": None,
              "stationID": None,
              "_nearbyStationsIDList": []
              }

    defaultParams = {
              "apiKey": None,
              "stationID": 13960,
              "_nearbyStationsIDList": []
              }

    forecast = None

    def isEnabledForLocation(self, timezone, lat, long):
        return WillyWeather.parserEnabled

    def perform(self):
        self.apiKey = self.params.get("apiKey", None)
        self.stationID = self.params.get("stationID", None)
        if self.apiKey is None or not self.apiKey or not isinstance(self.apiKey, str):
            self.lastKnownError = "Error: No API Key. Please register an account at https://www.willyweather.com.au/info/api.html"
            return

        self.params["_nearbyStationsIDList"] = []
        self.noDays = 7

        s = self.settings
        llat = s.location.latitude
        llon = s.location.longitude

        searchURL = "https://api.willyweather.com.au/v2/" + self.apiKey + "/search.json"
        searchURLParams = [
            ("lat", llat),
            ("lng", llon),
            ("units", "distance:km")
        ]

        try:
            d = self.openURL(searchURL, searchURLParams)
            if d is None:
                return

            search = json.loads(d.read())

            if self.parserDebug:
                log.info(search)

            self.getNearbyStations(search)

        except Exception, e:
            log.error("*** Error finding nearby stations")
            log.exception(e)

        if self.stationID is None:
            self.lastKnownError = "Error: No Station ID entered."
            return

        URL = "https://api.willyweather.com.au/v2/" + self.apiKey + "/locations/" + str(self.stationID) + "/weather.json"

        URLParams = [
            ("observational", "true"),
            ("forecasts", "weather,temperature,rainfall,wind"),
            ("days", self.noDays),
            {"units", "speed:m/s"}
        ]

        try:
            d = self.openURL(URL, URLParams)
            if d is None:
                return

            forecast = json.loads(d.read())

            if self.parserDebug:
                log.info(forecast)

            self.__getForecastData(forecast)


        except Exception, e:
            log.error("*** Error running WillyWeather parser")
            log.exception(e)

        log.debug("Finished running WillyWeather parser")

    def __getForecastData(self, forecast):
        datetime = forecast["observational"].get("issueDateTime")
        obstimestamp = rmTimestampFromDateAsString(datetime, '%Y-%m-%d %H:%M:%S')
        utcdatetime = rmTimestampToUtcDateAsString(obstimestamp)
        utctimestamp = rmTimestampFromDateAsString(utcdatetime, '%Y-%m-%d %H:%M:%S')

        otemp = forecast["observational"]["observations"]["temperature"].get("temperature")
        orain = forecast["observational"]["observations"]["rainfall"].get("todayAmount")
        ohumidity = forecast["observational"]["observations"]["humidity"].get("percentage")
        odp = forecast["observational"]["observations"]["dewPoint"].get("temperature")
        opressure = forecast["observational"]["observations"]["pressure"].get("pressure")

        if self.parserDebug:
            log.info("Current datetime:        %s" % datetime)
            log.info("Current local timestamp: %s" % obstimestamp)
            log.info("Current UTC:             %s" % utcdatetime)
            log.info("Current UTC timestamp:   %s" % utctimestamp)
            log.info("Current temp:     %s degrees C" % otemp)
            log.info("Current rain:     %s mm today" % orain)
            log.info("Current rel hum:  %s percent" % ohumidity)
            log.info("Current dewpoint: %s degrees C" % odp)
            log.info("Current pressure: %s kPa" % (opressure /10))

        self.addValue(RMParser.dataType.TEMPERATURE, obstimestamp, str(round(otemp, 2)))
        self.addValue(RMParser.dataType.RAIN, obstimestamp, orain)
        self.addValue(RMParser.dataType.RH, obstimestamp, ohumidity)
        self.addValue(RMParser.dataType.DEWPOINT, obstimestamp, odp)
        # Need to convery pressure from hPa to kPa
        self.addValue(RMParser.dataType.PRESSURE, obstimestamp, str(opressure / 10))

        day = 0

        while day < self.noDays:
            datetime = forecast["forecasts"]["weather"]["days"][day]["entries"][0].get("dateTime")
            timestamp = rmTimestampFromDateAsString(datetime, '%Y-%m-%d %H:%M:%S')
            utcdatetime = rmTimestampToUtcDateAsString(timestamp)
            utctimestamp = rmTimestampFromDateAsString(utcdatetime, '%Y-%m-%d %H:%M:%S')

            if self.parserDebug:
                log.info("Forecast Date: %s" % rmTimestampToDateAsString(timestamp))

            maxtemp = forecast["forecasts"]["weather"]["days"][day]["entries"][0].get("max")
            mintemp = forecast["forecasts"]["weather"]["days"][day]["entries"][0].get("min")

            for entry in forecast["forecasts"]["temperature"]["days"][day]["entries"]:
                datetime = entry.get("dateTime")
                timestamp = rmTimestampFromDateAsString(datetime, '%Y-%m-%d %H:%M:%S')
                utcdatetime = rmTimestampToUtcDateAsString(timestamp)
                utctimestamp = rmTimestampFromDateAsString(utcdatetime, '%Y-%m-%d %H:%M:%S')

                temperature = entry.get("temperature")

                self.addValue(RMParser.dataType.TEMPERATURE, timestamp, str(round(temperature, 2)))
                self.addValue(RMParser.dataType.MINTEMP, timestamp, str(round(mintemp, 2)))
                self.addValue(RMParser.dataType.MAXTEMP, timestamp, str(round(maxtemp, 2)))

            for entry in forecast["forecasts"]["wind"]["days"][day]["entries"]:
                datetime = entry.get("dateTime")
                timestamp = rmTimestampFromDateAsString(datetime, '%Y-%m-%d %H:%M:%S')
                utcdatetime = rmTimestampToUtcDateAsString(timestamp)
                utctimestamp = rmTimestampFromDateAsString(utcdatetime, '%Y-%m-%d %H:%M:%S')

                wind = entry.get("speed")

                self.addValue(RMParser.dataType.WIND, timestamp, str(round(wind, 2)))

            for entry in forecast["forecasts"]["rainfall"]["days"][day]["entries"]:
                datetime = entry.get("dateTime")
                timestamp = rmTimestampFromDateAsString(datetime, '%Y-%m-%d %H:%M:%S')
                utcdatetime = rmTimestampToUtcDateAsString(timestamp)
                utctimestamp = rmTimestampFromDateAsString(utcdatetime, '%Y-%m-%d %H:%M:%S')

                rainfallmin = entry.get("startRange")
                rainfallmax = entry.get("endRange")
                rainfallavg = (self.__toFloat(rainfallmin) + self.__toFloat(rainfallmax))/2

                self.addValue(RMParser.dataType.QPF, timestamp, rainfallavg)


            day += 1

        if self.parserDebug:
            log.debug(self.result)

    def getNearbyStations(self, jsonData):
        try:
            nearestStation = jsonData["location"].get("id")
        except:
            log.warning("No closest station found!")
            self.lastKnownError = "Warning: No closest station found!"
            return

        closestURL = "https://api.willyweather.com.au/v2/" + self.apiKey + "/search/closest.json"
        closestURLParams = [
            ("id", nearestStation),
            ("weatherTypes", "general"),
            ("units", "distance:km")
        ]

        try:
            d = self.openURL(closestURL, closestURLParams)
            if d is None:
                return

            closest = json.loads(d.read())

            if self.parserDebug:
                log.info(closest)

            for i in closest["general"]:
                id = i["id"]
                name = i["name"]
                region = i["region"]
                postcode = i["postcode"]
                distance = i["distance"]

                infoStr = "Station ID = " + str(id) + " (" + name + ", " + region + ", " + str(postcode) + ", " + str(distance) + " kms away)"

                self.params["_nearbyStationsIDList"].append(infoStr)
			
            if self.parserDebug:
                log.debug(self.params["_nearbyStationsIDList"])

        except Exception, e:
            log.error("*** Error running WillyWeather parser")
            log.exception(e)

    def __toFloat(self, value):
        if value is None:
            return 0
        return float(value)

if __name__ == "__main__":
    parser = WillyWeather()
    parser.perform()
