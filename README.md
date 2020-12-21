[![willyweather](https://img.shields.io/github/release/safepay/rainmachine-willyweather.svg)](https://github.com/safepay/rainmachine-willyweather) ![Maintenance](https://img.shields.io/maintenance/yes/2020.svg)

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
## Obtain an API Key from Willyweather
Go to https://www.willyweather.com.au/info/api.html.

Select "Single Location" and click "Next".

Select "Show sub-items" next to "Weather" to reveal the sub-menu.

Tick "Observational".

Select "Show sub-items" next to "Forecasts" to reveal the sub-menu.

Tick "Weather", "Temperature", "Wind" and "Rainfall" and click "Next".

![API Settings Screenshot](https://github.com/safepay/rainmachine-willyweather/raw/master/api_settings.png)

Complete the process with your own information, including your credit card.

There will now be an API Key on the API Admin page that you can use with RainMachine.

## Install and Configure RainMachine Parser
Download the willyweather.py file from the repository.

In the RainMachine UI, go to Settings --> Weather --> User uploaded.

Select "Add New" and browse to the willyweather.py file and then upload.

Click on the new parser to show the configuration items.

Press the DEFAULTS option to populate a temporary Station ID and to tick the LookUp Station Box.

Enter your WillyWeather API key and Save.

Hit REFRESH and a list of closest stations should appear magically in the UI.

Enter the one you want and SAVE again.

**Note: Once you REFRESH, RainMachine does not allow another refresh for 5 minutes, so please be patient with these steps.**

Once you have the system working with your chosen Station ID, you can set the flag "stationLookUp" off (false)
to stop the parser making the two additional API calls for the search capability. This will save cost and leave
a single API call every 4 hours, or when the device deems it necessary, to retrieve weather data.

## Troubleshooting if Station ID or API Key Won't Save
Sometimes RainMachine refuses to save the values for Station ID and/or API Key. This is not a parser bug, but a limitation of RainMachine.

If this happens, press the DEFAULTS button to populate the default values, then change to your own values and Save again. This should solve the problem. You may still need to do this more than once.

There is no fix for this from RainMachine.

## Troubleshooting if you can't find your station ID
If you have somehow gotten to a point where you can't find your station ID, you can get it from the page source of WillyWeather.
Just go to your location in WillyWeather. E.g. https://www.willyweather.com.au/vic/melbourne/melbourne.html

Then in your browser view the source (usually by right-clicking on the page).

Then search for ```ww.location```. This is quite close to the top of the source, so you can also scroll down.
You will see a number next to the ID field. E.g. ```ww.location = {"id":13960,"name":"Melbourne"``` gives a Station ID of ```13960```.

Enter this number in to RainMachine.
