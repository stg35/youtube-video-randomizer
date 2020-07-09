from pymongo import MongoClient
from secret_data import db_connect
from random import randint


client = MongoClient(db_connect)
db = client['yvr']

def updateVideos(videos):
    db['videos'].remove({})
    for i in videos:
        db['videos'].insert_one(i)

def randomVideo():
    end = db['videos'].find().sort('_id', -1).limit(1)[0]['_id'] + 1
    rand = randint(0, end)
    return db['videos'].find_one({'_id': rand})

