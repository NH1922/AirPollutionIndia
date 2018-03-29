from flask import Flask,render_template,flash,request,redirect
from wtforms import Form,TextField,TextAreaField,validators,StringField,SubmitField
import requests
import json
import time
import urllib.request
import config
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from time import sleep
from werkzeug.utils import redirect
from flask.helpers import url_for
#from boto.ec2.address import Address


#Functions to fecth the data from geocode

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

#Function to find air pollution data

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

app = Flask(__name__)
app.secret_key = "123456789"
Bootstrap(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class cityform(Form):
    name = StringField("City", validators=[validators.required()])
    submit = SubmitField("submit")
@app.route("/",methods = ["POST","GET"])
def HOME():
    #Setting up mongo db connections 
    client = MongoClient(config.mongohost, config.mongoport)
    #  name of the data base - AirReports
    db = client.AirReports
    form = cityform(request.form)
    reports = db.reports
    if request.method == "POST" and form.validate():
        city_names = form.name.data
        city_names = city_names.split(",")
        print(city_names)
        for city in city_names:
            lattitude,longitude = GEOLOCATION(city)
            report = POLLUTIONREPORT(lattitude, longitude,city)
            reports.insert_one(report)
            #print (report)
            #return render_template("result.html",report = report)
        
    else:
        print("faliure")

    return render_template("Home.html",form = form)
@app.route("/display")
def DISPLAY():
    client = MongoClient(config.mongohost, config.mongoport)
    db = client.AirReports
    reports = db.reports
    data = reports.find()
    cities = []
    for details in data:
        cities.append(details['city'])
    print(cities)
    return render_template("display.html",cities=cities)
@app.route("/data/<string:cityid>/")
def DATA(cityid):
    client = MongoClient(config.mongohost, config.mongoport)
    db = client.AirReports
    reports = db.reports
    for city in reports.find({'city':cityid}):
        print(city)
    return render_template("result.html",report = city)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)