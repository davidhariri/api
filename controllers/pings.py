import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
from config import settings
from markdown import markdown as HTML_from_markdown
import json

database = pymongo.MongoClient('mongodb://{}:{}{}'.format(settings["database"]["user"], settings["database"]["pass"], settings["database"]["url"]))["blog"]

class Ping(object):
    def __init__(self, logged=datetime.now(), time=None, lat=None, lon=None, **kwargs):
        self.logged = logged

        if isinstance(time, basestring):
            # Assume: "2016-03-05 14:27:34 +0000"
            parsed_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S +0000")
            self.time = parsed_time
        else:
            self.time = time

        self.location = {
            "x" : lon,
            "y" : lat
        }

    def save(self):
        try:
            database.pings.insert_one(self.__dict__)
        except Exception as e:
            print "Ping: Failed to insert new ping:"
            print e