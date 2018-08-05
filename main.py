from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import config
import cronjob
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread
from geolocation import GEOLOCATION
from pollutiondata import PollutionData

app = Flask(__name__)
app.secret_key = "123456789"
Bootstrap(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True


def schedule_calls():
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(cronjob.Update, 'interval', hours=1)
    scheduler.start()




class cityform(Form):
    name = StringField("City", validators=[validators.required()])
    submit = SubmitField("submit")


@app.route("/", methods=["POST", "GET"])
def HOME():
    # Setting up mongo db connections
    client = MongoClient(config.mongohost, config.mongoport)
    #  name of the data base - AirReports
    db = client.AirReports
    form = cityform(request.form)
    reports = db.reports
    if request.method == "POST" and form.validate():
        city_names = form.name.data
        city_names = city_names.split(",")
        print(city_names)
        threads = []
        pollutionreports = []
        newcities = []
        for city in city_names:
            if reports.find({'city': city}).count() != 0:
                continue;
            else:
                newcities.append(city)
        for city in newcities:
             t = Thread(target=GEOLOCATION, args=(city, pollutionreports))
             threads.append(t)
        for x in threads:
            x.start()
        for x in threads:
            x.join()
        print(pollutionreports)
        reports.insert_many(pollutionreports)
    else:
        print("faliure")
    schedule_calls()
    print("Function called ! ")
    return render_template("Home.html", form=form)


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
    return render_template("display.html", cities=cities)


@app.route("/data/<string:cityid>/")
def DATA(cityid):
    client = MongoClient(config.mongohost, config.mongoport)
    db = client.AirReports
    reports = db.reports
    for city in reports.find({'city': cityid}):
        print(city)
    return render_template("result.html", report=city)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
