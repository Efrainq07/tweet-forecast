from flask import jsonify
import database as dat
import pymongo as pm
import datetime as dt
import numpy as np




def mk_time_series(begin_datetime, end_datetime):

    #Accedemos a la coleccion donde estan los tweets del listener
    tweet_col = pm.collection.Collection(dat.db, 'tweet_listener')

    #Consulta a la base de datos para obtener tweets en un intervalo de fechas
    query = {
        "created_at_date" : {'$lt': end_datetime, '$gte': begin_datetime}
    }

    #Consulta
    result = tweet_col.find(query).sort("created_at_date",pm.ASCENDING)
    
    step = dt.timedelta(minutes = 10)
    current = begin_datetime
    count = 0

    for tweet in result:
        if (tweet["created_at_date"] >  current + step):
            count += 1
            current += step
        





def ARIMA():
    return jsonify({"status":"ok"})