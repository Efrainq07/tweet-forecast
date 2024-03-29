from flask import jsonify
from statsmodels.tsa.arima_model import ARIMA

import database as dat
import pymongo as pm
import datetime as dt
import numpy as np
import pandas as pd
import math as mt


''' query = {
        "created_at_date" : {'$lt': end_datetime, '$gte': begin_datetime}
        "entities" : { "hashtags" : {"$in" : [hashtag] } }
    }'''


def get_timeseries(hashtag, begin_datetime, end_datetime, time_step):

    #Accedemos a la coleccion donde estan los tweets del listener
    tweet_col = pm.collection.Collection(dat.db, hashtag)

    #Consulta a la base de datos para obtener tweets en un intervalo de fechas
    query = {
        "created_at_date" : {'$lt': end_datetime, '$gte': begin_datetime}
    }



    #Consulta
    result = tweet_col.find(query).sort("created_at_date",pm.ASCENDING)
    
    #Se estructuran los datos para tener el promedio de followers_count en cada time_step
    step = time_step
    current = begin_datetime
    curr_time = 0
    count = 0
    timeseries = [[0],[current]]

    for tweet in result:
        if (tweet["created_at_date"] >  current + step):
            timeseries[0][curr_time] /= count if count!=0 else 1
            count = 0
            curr_time += 1
            current += step
            timeseries[0].append(0)
            timeseries[1].append(current)
        count += 1
        timeseries[0][curr_time] += tweet['user']['followers_count']

    #Se regresa una lista
    return timeseries[0]
    




def forecast_ARIMA(timeseries,length,param):
    try:
        model = ARIMA(timeseries, order=param)
    except:
        return "No hay suficientes registros para hacer esa predicción."
    model_fit = model.fit(disp=0)
    output = model_fit.predict(start = len(timeseries), end = len(timeseries)+length)
    clean = [i if i>=0 else 0 for i in output.tolist()]
    return clean
