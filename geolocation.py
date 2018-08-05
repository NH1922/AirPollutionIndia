import config
import urllib.request
import json
from pollutiondata import PollutionData
from threading import Thread

def GEOLOCATION(address,pollutionreports):
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+config.geo_api_key
    geo_response = urllib.request.urlopen(geo_url).read()
    geo_json_obj = str(geo_response,'utf-8')
    geo_data=json.loads(geo_json_obj)
    res = {}
    for keys in geo_data['results']:
        res.update(keys)
    lattitude,longitude = str(res['geometry']['location']['lat']),str(res['geometry']['location']['lng'])
    result = list([lattitude,longitude])
    PollutionData(result,address,pollutionreports)

    #geocodelist.append(list([str(res['geometry']['location']['lat']),str(res['geometry']['location']['lng'])]))


