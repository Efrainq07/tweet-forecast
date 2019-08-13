import pymongo as pm
import json
import ssl

with open("credentials.json", "r") as file:
    creds = json.load(file)

mongo = pm.MongoClient(creds['database_connect']['URI'], maxPoolSize=50, connect=False, ssl_cert_reqs=ssl.CERT_NONE)
db = pm.database.Database(mongo, creds['database_connect']['database_name'])