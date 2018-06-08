import json
from pymongo import MongoClient
import config
import urllib.request


client = MongoClient(config.mongohost, config.mongoport)
db = client.AirReports
reports = db.reports



def PollutionData(address,option):
    '''Finding lattitude and longitude using google's geolocation api '''
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+config.geo_api_key
    geo_response = urllib.request.urlopen(geo_url).read()
    geo_json_obj = str(geo_response,'utf-8')
    geo_data=json.loads(geo_json_obj)
    res = {}
    for keys in geo_data['results']:
        res.update(keys)
    lattitude,longitude = str(res['geometry']['location']['lat']),str(res['geometry']['location']['lng'])

    '''Using air pollution api to fetch data'''
    url="http://api.airpollutionapi.com/1.0/aqi?"
    request_url = url + "lat="+lattitude+"&"+"lon="+longitude+"&APPID="+config.apikey
    response = urllib.request.urlopen(request_url).read()
    json_obj = str(response,'utf-8')
    pollution_data = json.loads(json_obj)
    city = {'city':address}
    report = ({**city,**pollution_data})
    if(option=='U'):
        reports.update({'city': city}, report)
        print("City updated!")
    else:
        reports.insert_one(report)
        print("City inserted !")
