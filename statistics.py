from flask import jsonify
from statsmodels.tsa.arima_model import ARIMA

import database as dat
import pymongo as pm
import datetime as dt
import numpy as np
import pandas as pd





def get_time_series(begin_datetime, end_datetime, time_step):

    #Accedemos a la coleccion donde estan los tweets del listener
    tweet_col = pm.collection.Collection(dat.db, 'tweet_listener')

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
    timeseries = np.array([[0],[current]])

    for tweet in result:
        if (tweet["created_at_date"] >  current + step):
            timeseries[curr_time] /= count
            count = 0
            curr_time += 1
            current += step
            timeseries = np.append(timeseries,0)
            timeseries = np.append(timeseries,current)
        count += 1
        timeseries[curr_time] += tweet['user']['followers_count']

    #Se regresa un DataFrame de pandas
    return pd.DataFrame({ 'datetime': timeseries[1], 'avg_followers_count': timeseries[0]})
    




def forecast_ARIMA(timeseries,length,param):
    model = ARIMA(timeseries, order=param)
    model_fit = model.fit(disp=0)
    output = model_fit.predict(start = len(timeseries), end = len(timeseries)+length)
    return output