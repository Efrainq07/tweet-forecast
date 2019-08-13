import statistics as st
import database as dat
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
def home():
        if request.method == 'GET':
                query = request.args.to_dict()
                insert = twitter.search(**query)['statuses']
                for doc in insert:
                        formating = "%a %b %d %H:%M:%S %z %Y"
                        created_at_date = datetime.datetime.strptime(doc['created_at'],formating)
                        doc["created_at_date"] = created_at_date
                ret = jsonify(insert)
                tweet_col.insert_many(insert)
                return ret



@app.route('/forecast', methods =['GET'])
def forecast():
        return st.ARIMA()
