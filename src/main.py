from satviewlib import DataDownloader, TimeUtils
import st7735
from PIL import Image
import time, re


def getLatestTime(time_downloader):
    time_downloader.request()
    return (re.search("<Domain>(.*)</Domain>", time_downloader.getAsTextData()).group(1))[26:50]


tft = st7735.ST7735(offset_left=-1, offset_top=1, port=0, cs=0, dc=23, backlight=None, rst=18, width=128, height=160, rotation=270, invert=False)

map_req = {
    "SERVICE"      : "WMS",
    "VERSION"      : "1.3.0",
    "REQUEST"      : "GetMap",
    "LAYERS"       : ["msg_iodc:rgb_naturalenhncd", "msg_fes:h60b"],
    "WIDTH"        : 160,
    "HEIGHT"       : 128,
    "FORMAT"       : "image/png",
    "BBOX"         : [20, -15, 60, 45],
    "SRS"          : "EPSG:4326",
    "TIME"         : "",
    "TRANSPARENT"  : "true",
}


time_req = {
    "SERVICE"      : "WMTS",
    "VERSION"      : "1.0.0",
    "REQUEST"      : "DescribeDomains",
    "LAYER"        : "msg_iodc:rgb_naturalenhncd",
    "FORMAT"       : "image/png",
    "DOMAINS"      : "time"
}


img_downloader = DataDownloader(params=map_req, base_url="https://view.eumetsat.int/geoserver/")
time_downloader = DataDownloader(params=time_req, base_url="https://view.eumetsat.int/geoserver/gwc/service/")
time_downloader.makeUrl()

last_time = ""
current_time = getLatestTime(time_downloader)

img_downloader.setParameter("TIME", current_time)

while True:
    if not last_time == current_time:
        img_downloader.makeUrl()
        img_downloader.request()
        image = img_downloader.getAsImage()
        R, G, B = image.convert("RGB").split()
        tft.display(Image.merge("RGB", (B, G, R)))
        
        last_time = current_time
    
    if int(time.strftime("%M", time.localtime())) % 15 == 0: 
        time.sleep(10)
        current_time = getLatestTime(time_downloader)
        img_downloader.setParameter("TIME", current_time)
    
    time.sleep(30)

