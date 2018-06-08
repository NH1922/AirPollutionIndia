import requests
import json
import time
import urllib.request
import config
import main
from pymongo import MongoClient
from pollution_report import PollutionData


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
        report = PollutionData(city)
        reports.update({'city':city},report)
    print ("Cron job called ! ")
