# rpi-satellite-data-viewer
View live satellite data on a tft screen using a raspberry pi  

This project uses the following library for controlling the tft screen: st7735 -> https://github.com/pimoroni/st7735-python  


DataDownloader class  
.setParameters(parameters) -> set a dictionary of parameters for the http request.  
.setParameter(parameter, value) -> set a single key:value pair in the http request dictionary.  
.makeUrl() -> uses the dictionary to create the http request, and stores it in the final_url variable.  
.request() -> sends the request and stores the data in response variable.  
.getAsTextData() -> returns the response as a string.  
.getAsBinaryData() -> returns the response as a byte object.  
.getAsImage() -> returns the response as an image.  


TimeUtils class  
.toIntTime(time_str) -> converts a string containing the time into an array containing the year, month, day, hour and minute.  
.toStringTime(year, month, day, hour, minute) -> returns the time given as a string.  
