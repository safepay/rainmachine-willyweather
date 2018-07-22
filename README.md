# Rainmachine Willyweather Australia Parser
A parser for the RainMachine smart watering system using the API from www.willyweather.com.au

Note that I am not a professional (or even amateur!!) programmer.
I wrote this because of the lack of local Australian support from the RainMachine system.
However, the built in global parsers do a pretty good job.

The Willyweather service is a commercial API with the first 5000 calls free, then a cost based on the type of data you want to access.
The typical cost is aroung $0.09 per 1000 calls for a single weather station, which is what the code is written to handle.

If you have any suggestions or can clean up my code then thanks in advance!

The main confusion I have is how RainMachine stores time. That is why the code has references to both local and UTC time, but I am logging with local so that my data matches that from services such as OpenWeatherMaps.

Register for the Willyweather API
=================================
Go to https://www.willyweather.com.au/info/api.html
Select "Single Location" and click "Next"
Select "Show sub-items" next to "Weather" to reveal the sub-menu
Tick "Observational"
Select "Show sub-items" next to "Forecasts" to reveal the sub-menu
Tick "Weather", "Temperature", "Wind" and "Rainfall" and click "Next"
Complete the process with your own information, including your credit card.


Installation
============
In the RainMachine UI, go to Settings --> Weather --> User uploaded
Select "Add New" and browse to the willyweather.py file and then upload.
You then need to enter your WillyWeather API key.
The hit REFRESH a few times and a list of closest stations should appear magically in the UI.
Enter the one you want and SAVE.
If nothing saves, then press the DEFAULTS button to populate the default value, then change to your own.
Sorry for the convoluted instructions, but this is the only way I could get it to save the Station ID properly.

Note for Windows Users
======================
If you upload from Windows you will get an error.
Renaming the file to willyweather.txt will result in a successful upload.
But... if you then reboot RainMachine you will lose the parser (sad face).

You can only get this to work from a Linux or similar OS.
