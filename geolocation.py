import config
import urllib.request
import json
from pollutiondata import pollution_data
from threading import Thread
import geocoder

def geolocation(address, pollution_reports):
    g = geocoder.google(address)
    #lattitude,longitude = g.latlng
    #print(lattitude,longitude)
    #result = list([lattitude,longitude])
    print(g.latlng)
    pollution_data(g.latlng, pollution_reports, address)

    #geocodelist.append(list([str(res['geometry']['location']['lat']),str(res['geometry']['location']['lng'])]))


