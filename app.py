import statistics as st
import database as dat
import utils as ut
import datetime

from flask import Flask, request, jsonify
from twython import Twython
import json
import pymongo as pm
from bson.json_util import dumps


with open("credentials.json", "r") as file:
        creds = json.load(file)


tweet_col = pm.collection.Collection(dat.db, 'tweet_listener')
twitter = Twython(creds['twitter_token']['CONSUMER_KEY'], creds['twitter_token']['CONSUMER_SECRET'])


app = Flask(__name__)

@app.route('/upload', methods = ['GET','POST'])
def upload():
        if request.method == 'GET':
                query = request.args.to_dict()
                insert = twitter.search(**query)['statuses']
                insert = ut.add_timestamp(insert)
                ret = jsonify(insert)
                tweet_col.insert_many(insert)
                return ret



@app.route('/forecast', methods =['GET'])
def forecast():
        formating_date = "%m-%d-%y %H:%M:%S"
        formating_step = "%H:%M:%S"
        query = request.args.to_dict()
        begin_date = datetime.datetime.strptime(query['begin_date'],formating_date)
        end_date = datetime.datetime.strptime(query['end_date'],formating_date)
        timestep = datetime.datetime.strptime(query['begin_date'],formating_step)
        timestep = datetime.timedelta(hours=timestep.hour, minutes=timesetep.minute, seconds=timestep.second)
        length = query['length']
        param = (5,1,0)

        timeseries = st.get_timeseries(begin_date,end_date,time_step)
        forecast = st.forecast_ARIMA(timeseries,length,param)

        return jsonify({"forecast":forecast})

