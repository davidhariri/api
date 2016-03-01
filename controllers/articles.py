import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from datetime import datetime
from config import settings
from markdown import markdown as HTML_from_markdown

database = pymongo.MongoClient('mongodb://{}:{}{}'.format(settings["database"]["user"], settings["database"]["pass"], settings["database"]["url"]))["blog"]

class Article(object):
    def __init__(self, _id=ObjectId(), key=None, title="", text="", made=datetime.now(), updated=datetime.now(), tags=[], published=False, content=None):
        if content == None:
            self.content = {
                "html" : "",
                "markdown" : text
            }
        else:
            self.content = content

        if isinstance(_id, ObjectId):
            self._id = _id
        elif isinstance(_id, basestring):
            self._id = ObjectId(_id)
        else:
            self._id = ObjectId()

        self.key = key
        self.title = title

    def set_text(self, new_text):
        self.content["markdown"] = new_text
        self.content["html"] = HTML_from_markdown(new_text)
        self.updated = datetime.now()

    def set_title(self, new_title):
        self.title = new_title
        self.updated = datetime.now()

    def set_key(self, new_key):
        self.key = new_key
        self.updated = datetime.now()

    def set_published(self, new_published):
        self.published = new_published
        self.updated = datetime.now()

    def get_json(self):
        return dumps(self)

def find(_id=None, key=None, only_published=True):
    # Find an article in various ways and return a list of Article's
    # Favoring _id > key

    # Append a published flag if specified
    def get_published_flag():
        if only_published:
            return {"published" : True}.items()

        return {}.items()

    def get_search_results_from_search(search):
        results = []

        try:
            db_results = database.articles.find(search)

            for result in db_results:
                results.append(Article(**result))

        except Exception as e:
            print "Could not make search:"
            print e

        return results

    if isinstance(_id, ObjectId):
        search = dict({"_id" : _id}.items() + get_published_flag())
        return get_search_results_from_search(search)

    elif isinstance(key, basestring):
        search = dict({"key" : key}.items() + get_published_flag())
        return get_search_results_from_search(search)

    else:
        print "Cannot find article. No searchable attribute passed"

    return None

def save(article):
    if isinstance(article, Article):
        try:
            database.articles.update({"_id" : article._id}, {"$set" : article.__dict__}, True)
            return article

        except Exception as e:
            print "Could not save Article. Database Error:"
            print e

    else:
        print "Could not save Article. Object not of type Article"

    return False

def delete(article):
    if isinstance(article, Article):
        try:
            database.articles.delete_one({"_id" : article._id})
            return article

        except Exception as e:
            print "Could not delete Article. Database Error:"
            print e

    else:
        print "Could not delete Article. Object not of type Article"

    return False
