import json
import config
import urllib.request

def PollutionData(latlong,pollutionreports,address):
    '''Using air pollution api to fetch data'''
    lattitude,longitude = latlong
    url = "http://api.airpollutionapi.com/1.0/aqi?"
    request_url = url + "lat=" + str(lattitude) + "&" + "lon=" + str(longitude) + "&APPID=" + config.apikey
    print(request_url)
    response = urllib.request.urlopen(request_url).read()
    json_obj = str(response, 'utf-8')
    pollution_data = json.loads(json_obj)
    city = {'city': address}
    report = ({**city, **pollution_data})
    print(report)
    pollutionreports.append(report)


    '''if (option == 'U'):
        reports.update({'city': city}, report)
        print("City updated!")
    else:
        reports.insert_one(report)
        print("City inserted !")'''