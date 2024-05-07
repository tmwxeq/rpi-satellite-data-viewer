import requests
from PIL import Image
import io
from datetime import datetime, timedelta

class DataDownloader:
    def __init__(self, params={"SERVICE" : "WMS", "REQUEST" : "GetCapabilities"}, base_url="https://view.eumetsat.int/geoserver/"):
        self.base_url = base_url
        self.params = params
        self.final_url = ""
    

    def setParameters(self, parameters):
        self.params = parameters
    

    def setParameter(self, parameter, value):
        self.params[parameter] = value
    

    def makeUrl(self):
        self.final_url = self.base_url
        self.final_url += self.params["SERVICE"].lower()
        self.final_url += "?"
        for parameter in self.params:
            param_value = self.params[parameter]
            if (type(param_value) == str or type(param_value) == int) and not param_value == "":
                self.final_url += parameter
                self.final_url += "="
                self.final_url += str(self.params[parameter])
                self.final_url += "&"
            elif type(param_value) == list and not param_value == []:
                self.final_url += parameter
                self.final_url += "="
                for coordinate in self.params[parameter]:
                    self.final_url += str(coordinate)
                    self.final_url += ","
                self.final_url = self.final_url[:-1]
                self.final_url += "&"
        self.final_url = self.final_url[:-1]
    

    def request(self):
        print("Making HTTP request...")
        self.response = requests.get(self.final_url)
        if not self.response:
            raise Exception("HTTP get request error code:", self.response.status_code)
    

    def getAsTextData(self):
        return self.response.text
    

    def getAsBinaryData(self):
        return self.response.content
    

    def getAsImage(self):
        image = Image.open(io.BytesIO(self.getAsBinaryData()))
        return image


class TimeUtils:
    def toIntTime(time_str):
        year = int(time_str[0:4])
        month = int(time_str[5:7])
        day = int(time_str[8:10])
        hour = int(time_str[11:13])
        minute = int(time_str[14:16])
        return [year, month, day, hour, minute]


    def toStringTime(year, month, day, hour, minute):
        month_str = str(month)
        day_str = str(day)
        hour_str = str(hour)
        minute_str = str(minute)
        if month < 10: month_str = f'0{month}'
        if day < 10: day_str = f'0{day}'
        if hour < 10: hour_str = f'0{hour}'
        if minute < 10: minute_str = f'0{minute}'
        return f'{year}-{month_str}-{day_str}T{hour_str}:{minute_str}:00.000Z'

