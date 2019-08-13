import datetime

def add_timestamp(insert):
    for doc in insert:
        formating = "%a %b %d %H:%M:%S %z %Y"
        created_at_date = datetime.datetime.strptime(doc['created_at'],formating)
        doc["created_at_date"] = created_at_date
    return insert