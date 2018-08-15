from flask import Flask, render_template, flash, request, redirect
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf import Form
import config
import cronjob
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread
from geolocation import geolocation
from pollutiondata import pollution_data

app = Flask(__name__)
app.secret_key = "123456789"
Bootstrap(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True


def schedule_calls():
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(cronjob.update, 'interval', hours=2)
    scheduler.start()




class city_form(Form):
    name = StringField("City", validators=[validators.required()])
    #submit = SubmitField("SUBMIT")


@app.route("/", methods=["POST", "GET"])
def home():
    # Setting up mongo db connections
    client = MongoClient(config.mongohost, config.mongoport)
    #  name of the data base - AirReports
    db = client.AirReports
    form = city_form(request.form)
    reports = db.reports
    if request.method == "POST" and form.validate():
        city_names = form.name.data
        city_names = city_names.split(",")
        print(city_names)
        threads = []
        pollution_reports = []
        new_cities = []
        for city in city_names:
            if reports.find({'city': city}).count() != 0:
                continue;
            else:
                new_cities.append(city)
        for city in new_cities:
             t = Thread(target=geolocation, args=(city, pollution_reports))
             threads.append(t)
        for x in threads:
            x.start()
        for x in threads:
            x.join()
        print(pollution_reports)
        reports.insert_many(pollution_reports)
    else:
        print("faliure")
    schedule_calls()
    print("Function called ! ")
    return render_template("Home.html", form=form)


@app.route("/display")
def display():
    client = MongoClient(config.mongohost, config.mongoport)
    db = client.AirReports
    reports = db.reports
    data = reports.distinct('city')
    cities = []
    for details in data:
        cities.append(details)
    print(cities)
    return render_template("display.html", cities=cities)


@app.route("/data/<string:cityid>/")
def data(cityid):
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
