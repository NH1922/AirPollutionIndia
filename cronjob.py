import config
from pymongo import MongoClient
from pollutiondata import pollution_data
from threading import Thread

client = MongoClient(config.mongohost, config.mongoport)
db = client.AirReports
reports = db.reports

def update():
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
        t = Thread(target=pollution_data, args=(latlongs[i], polltionreports, cities[i]))
        threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    for details in polltionreports:
        print(details)

    reports.insert_many(polltionreports)

    '''report = PollutionData(city)
        reports.update({'city':city},report)'''
    print ("Cron job called ! ")

data = reports.distinct('city')
print(data)

for data in  reports.find({'city':'Panaji'}):
    print(data)