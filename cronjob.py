import requests
import json
import time
import urllib.request
import config
import main
from pymongo import MongoClient
#from pollution_report import PollutionData
from pollutiondata import PollutionData
from threading import Thread

def Update():
    client = MongoClient(config.mongohost, config.mongoport)
    db = client.AirReports
    reports = db.reports
    data = reports.find()
    cities = []
    latlongs = []
    threads = []
    polltionreports=[]
    for details in data:
        cities.append(details['city'])
        latlongs.append(list([(details['data']['coordinates']['latitude']),
                              details['data']['coordinates']['longitude']]))
    print(cities)
    for i in range (len(cities)):
        t = Thread(target=PollutionData,args=(latlongs[i],polltionreports,cities[i]))
        threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    for details in polltionreports:
        print(details)
        reports.update({'city':details['city']},details)

        '''report = PollutionData(city)
        reports.update({'city':city},report)'''
    print ("Cron job called ! ")


