from flask import Flask,render_template,flash,request,redirect
from wtforms import Form,TextField,TextAreaField,validators,StringField,SubmitField
import requests
import json
import time
import urllib.request
import config

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

class cityform(Form):
    name = StringField("City", validators=[validators.required()])
    submit = SubmitField("submit")
@app.route("/",methods = ["POST","GET"])
def  HOME():
    form = cityform(request.form)
    if request.method == "POST" and form.validate():
        city = form.name.data
        print(city)
        lattitude,longitude = GEOLOCATION(city)
        report = POLLUTIONREPORT(lattitude, longitude,city)
        print (report)
        return render_template("result.html",report = report)
        flash("success !")
    else:
        print("faliure")

    return render_template("Home.html",form = form)




if __name__ == "__main__":
    app.run(debug = True)
