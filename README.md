[![willyweather](https://img.shields.io/github/release/safepay/rainmachine-willyweather.svg)](https://github.com/safepay/rainmachine-willyweather) ![Maintenance](https://img.shields.io/maintenance/yes/2019.svg)

# RainMachine Australian Bureau of Meteorology Parser
A parser for the RainMachine smart watering system using the API from www.willyweather.com.au which provides a commercial Json API for  Australian Bureau of Meteorology data.

I wrote this due to lack of local Australian support from the RainMachine system.
However, the built in global parsers do a pretty good job. I personally use this as my sole parser with good results. Most of the other parsers give conflicting local data. I would suggest trialling all the viable parsers and then using the ones with which you are most confident.

The Willyweather service, while being commercial, is very inexpensive, with the first 5000 calls free, then a cost based on the type of data you want to access.
The typical cost is around $0.04 to $0.05 per 1000 calls for a single weather station, which is what the code is written to handle. But as the parser only runs 4 times per day, it will take about 3 years to use your 5000 freebies.

If you have any suggestions for changes or additions then please let me know.

## Parser Features
* Search for nearby weather data and provide station ID
* Entry of preferrred local station ID
* Supports the following forecast data:
  * Rain amount
  * Rain probability
  * High/low temperatures
  * Hourly temperature
  * Hourly wind
* Provides total rainfall for previous day
* Supports home screen weather icons

# Installation
## Register for the Willyweather API
Go to https://www.willyweather.com.au/info/api.html.

Select "Single Location" and click "Next".

Select "Show sub-items" next to "Weather" to reveal the sub-menu.

Tick "Observational".

Select "Show sub-items" next to "Forecasts" to reveal the sub-menu.

Tick "Weather", "Temperature", "Wind" and "Rainfall" and click "Next".

![API Settings Screenshot](https://github.com/safepay/rainmachine-willyweather/raw/master/willyweather_api_settings.png)

Complete the process with your own information, including your credit card.

## Installation
Download the willyweather.py file from the repository.

In the RainMachine UI, go to Settings --> Weather --> User uploaded.

Select "Add New" and browse to the willyweather.py file and then upload.

You then need to enter your WillyWeather API key.

Hit REFRESH a few times and a list of closest stations should appear magically in the UI.

Enter the one you want and SAVE.

If nothing saves, then press the DEFAULTS button to populate the default value, then change to your own.

Once you have the system working with your chosen Station ID, you can set the flag "stationLookUp" off (false)
to stop the parser making the two additional API calls for the search capability. This will save cost and leave
a single API call every 4 hours, or when the device deems it necessary, to retrieve weather data.

## Note for Windows Users
If you upload from Windows you will get an error.
Renaming the file to willyweather.txt will result in a successful upload.
But... if you then reboot RainMachine you will lose the parser.

You can only get this to work from a Linux or similar OS (I believe Macs work but I have not tested this). This is a known bug in the RainMachine UI.
