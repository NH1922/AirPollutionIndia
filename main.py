import requests
import json
import time 
import urllib.request 

geo_api_key = "AIzaSyA4bfPbRZwKSt-nyepPMtIZmfWEVrzONb4"
address = "abhohar"
geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+geo_api_key

geo_response = urllib.request.urlopen(geo_url).read()
geo_json_obj = str(geo_response,'utf-8')
geo_data=json.loads(geo_json_obj)
res = {}
for keys in geo_data['results']:
    res.update(keys)
lattitude,longitude = str(res['geometry']['location']['lat']),str(res['geometry']['location']['lng'])

url="http://api.airpollutionapi.com/1.0/aqi?"
apikey = "m416esdc8pgggak1j8ou38v817"
#lattitude = "28.7040590"
#longitude = "77.10249"

request_url = url + "lat="+lattitude+"&"+"lon="+longitude+"&APPID="+apikey
response = urllib.request.urlopen(request_url).read()
json_obj = str(response,'utf-8')
pollution_data = json.loads(json_obj)
for key,value in pollution_data['data'].items():
    print(key,":",value)
    