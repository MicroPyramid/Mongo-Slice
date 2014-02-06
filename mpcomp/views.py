from json.encoder import JSONEncoder
from bson.objectid import ObjectId
import datetime
import json
from bson import json_util
import string
import random


def getConn(request):
    import pymongo

    client = pymongo.MongoClient(request.session['host'], request.session['port'])
    db = client[request.session['db']]
    db.authenticate(request.session['uid'], request.session['pwd'])
    return db


def mongoauth(host, port, db, uid, pwd):
    import pymongo
    print host, port, db, uid, pwd
    if host=="" or host is None or port=="" or port is None or db=="" or db is None or  uid=="" or uid is None or pwd=="" or pwd is None:
        return False

    try:
        client = pymongo.MongoClient(host,int(port))
        db = client[db]
        db.authenticate(uid, pwd)
        return True
    except pymongo.errors.PyMongoError:
        return False

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return json.dumps(obj, default=json_util.default)
        else:
            return JSONEncoder.default(obj, **kwargs)


def rand_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def getNextSequence(name):
    db =  mongoconnection()
    info = db.counter.find_and_modify(query={'_id': name },update={'$inc': { 'seq': 1 }},upsert=True,new=True)
    return info['seq']

