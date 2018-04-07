import requests
import json
import time
import urllib.request
import config
import main
from pymongo import MongoClient

def Update():
    client = MongoClient(config.mongohost, config.mongoport)
    db = client.AirReports
    reports = db.reports
    data = reports.find()
    cities = []
    for details in data:
        cities.append(details['city'])
    print(cities)

    for city in cities:
        lattitude,longitude = main.GEOLOCATION(city)
        report = main.POLLUTIONREPORT(lattitude, longitude,city)
        reports.update({'city':city},report)
    print ("Cron job called ! ")
