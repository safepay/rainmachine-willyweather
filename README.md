# Rainmachine Willyweather Australia Parser
A parser for the RainMachine smart watering system using the API from www.willyweather.com.au which provides a commercial Json API for the Australian Bureau of Meteorology data.

Note that I am not a professional (or even amateur!!) programmer.
I wrote this because of the lack of local Australian support from the RainMachine system.
However, the built in global parsers do a pretty good job. I personally use this parser and the Open Weather Map parser with good results.

The Willyweather service is a commercial API with the first 5000 calls free, then a cost based on the type of data you want to access.
The typical cost is around $0.05 per 1000 calls for a single weather station, which is what the code is written to handle. But as the parser only runs 4 times per day, it will take about 3.4 years to use your 5000 freebies.

If you have any suggestions or can clean up my code then thanks in advance!

## Register for the Willyweather API
Go to https://www.willyweather.com.au/info/api.html.

Select "Single Location" and click "Next".

Select "Show sub-items" next to "Weather" to reveal the sub-menu.

Tick "Observational".

Select "Show sub-items" next to "Forecasts" to reveal the sub-menu.

Tick "Weather", "Temperature", "Wind" and "Rainfall" and click "Next".

Complete the process with your own information, including your credit card.


## Installation
Download the willyweather.py file from the repository using the RAW --> Save As function. Make sure it has the .py extension.

In the RainMachine UI, go to Settings --> Weather --> User uploaded.

Select "Add New" and browse to the willyweather.py file and then upload.

You then need to enter your WillyWeather API key.

Hit REFRESH a few times and a list of closest stations should appear magically in the UI.

Enter the one you want and SAVE.

If nothing saves, then press the DEFAULTS button to populate the default value, then change to your own.

Once you have the system working with your chosen Station ID, you can set the flag "stationLookUp" off (false)
to stop the parser making the two additional API calls for the search capability. This will save cost and leave
a single API call every 4 hours to retrieve weather data.

## Note for Windows Users
If you upload from Windows you will get an error.
Renaming the file to willyweather.txt will result in a successful upload.
But... if you then reboot RainMachine you will lose the parser (sad face).

You can only get this to work from a Linux or similar OS. This is a known bug in the Rainmachine UI.
