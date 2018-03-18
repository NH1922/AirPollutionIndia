import requests
import json
import time 
import urllib.request 
import config




def GEOLOCATION(address):
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+config.geo_api_key
    geo_response = urllib.request.urlopen(geo_url).read()
    geo_json_obj = str(geo_response,'utf-8')
    geo_data=json.loads(geo_json_obj)
    res = {}
    for keys in geo_data['results']:
        res.update(keys)
    lattitude,longitude = str(res['geometry']['location']['lat']),str(res['geometry']['location']['lng'])
    return lattitude,longitude   

def POLLUTIONREPORT(lattitude,longitude):
    url="http://api.airpollutionapi.com/1.0/aqi?"
    request_url = url + "lat="+lattitude+"&"+"lon="+longitude+"&APPID="+config.apikey
    response = urllib.request.urlopen(request_url).read()
    json_obj = str(response,'utf-8')
    pollution_data = json.loads(json_obj)
    #for key,value in pollution_data['data'].items():
        #print(key,":",value)
    print("Air Quality :",pollution_data['data']['text'])
    print("Alert :",pollution_data['data']['alert'])
    print("Value :",pollution_data['data']['value'])
    print("Temperature :",pollution_data['data']['temp'])
    
    

address = input("City >")

lattitude,longitude = GEOLOCATION(address)
POLLUTIONREPORT(lattitude, longitude)


    