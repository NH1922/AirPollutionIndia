import config
import urllib.request
import json
from pollutiondata import PollutionData
from threading import Thread
import geocoder

def GEOLOCATION(address,pollutionreports):
    g = geocoder.google(address)
    #lattitude,longitude = g.latlng
    #print(lattitude,longitude)
    #result = list([lattitude,longitude])
    print(g.latlng)
    PollutionData(g.latlng,pollutionreports,address)

    #geocodelist.append(list([str(res['geometry']['location']['lat']),str(res['geometry']['location']['lng'])]))


