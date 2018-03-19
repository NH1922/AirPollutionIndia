import requests
import json
import time 
import urllib.request 
import config
from pymongo import MongoClient
from boto.ec2.address import Address

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

def POLLUTIONREPORT(lattitude,longitude,address):
    url="http://api.airpollutionapi.com/1.0/aqi?"
    request_url = url + "lat="+lattitude+"&"+"lon="+longitude+"&APPID="+config.apikey
    response = urllib.request.urlopen(request_url).read()
    json_obj = str(response,'utf-8')
    pollution_data = json.loads(json_obj)
    #for key,value in pollution_data['data'].items():
        #print(key,":",value)
    return{"city":address,"Quality":pollution_data['data']['text'],"Alert":pollution_data['data']['alert'],"Value":pollution_data['data']['value'],"Temperature":pollution_data['data']['temp']}
    #print("Quality :",pollution_data['data']['text'])
    #print("Alert :",pollution_data['data']['alert'])
    #print("Value :",pollution_data['data']['value'])
    #print("Temperature :",pollution_data['data']['temp'])
    
    
#Setting up mongo db connections 
client = MongoClient(config.mongohost, config.mongoport)
#  name of the data base - AirReports
db = client.AirReports
address = input("City >")
lattitude,longitude = GEOLOCATION(address)
reports = db.reports
report = POLLUTIONREPORT(lattitude, longitude,address)
reports.insert_one(report)
for key, value in report.items():
    print(key,":",value)

    