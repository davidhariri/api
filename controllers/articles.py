import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
from config import settings
from markdown import markdown as HTML_from_markdown
import json

database = pymongo.MongoClient('mongodb://{}:{}{}'.format(settings["database"]["user"], settings["database"]["pass"], settings["database"]["url"]))["blog"]

class Article(object):
    def __init__(self, _id=ObjectId(), title="", made=None, updated=None, tags=[], published=False, shared=False, content=None, read_count=0, love_count=0, **kwargs):
        # Content checker
        if isinstance(content, dict) is False:
            self.content = {
                "html" : "",
                "markdown" : ""
            }
        else:
            self.content = content

        # Id checker
        if isinstance(_id, ObjectId):
            self._id = _id
        elif isinstance(_id, basestring):
            self._id = ObjectId(_id)
        elif isinstance(_id, dict):
            self._id = ObjectId(_id["$oid"])
        else:
            self._id = ObjectId()

        now = datetime.now()

        # Date checker
        if isinstance(updated, dict):
            self.updated = datetime.fromtimestamp(updated["$date"] / 1000)
        elif updated is not None:
            self.updated = updated
        else:
            self.updated = now

        if isinstance(made, dict):
            self.made = datetime.fromtimestamp(made["$date"] / 1000)
        elif made is not None:
            self.made = made
        else:
            self.made = now

        self.title = title
        self.tags = tags
        self.published = published
        self.shared = shared
        self.read_count = read_count
        self.love_count = love_count

    def render_html(self):
        self.content["html"] = HTML_from_markdown(self.content["markdown"], extensions=["fenced_code"])
        self.updated = datetime.now()

def find(_id=None, authenticated=False):
    # Find an article in various ways and return a list of Article's

    # If no search query parameters specified then will just return latest articles
    # Append a published flag if specified

    def get_search_results_from_search(search):
        results = []

        try:
            db_results = database.articles.find(search).sort("_id", -1)

            for result in db_results:
                results.append(Article(**result))

        except Exception as e:
            print "Could not make search:"
            print e

        return results

    if isinstance(_id, basestring):
        # Accessing an article by it's id
        search = None

        if authenticated:
            # We have authentication so return anything that matches the _id
            search = dict({"_id" : ObjectId(_id)})
        else:
            # We don't have authentication so only return things that are shared
            #  or published (this rule only applies to direct access to links)
            search = {
                "$or" : [
                    {"_id" : ObjectId(_id), "shared" : True},
                    {"_id" : ObjectId(_id), "published" : True}
                ]
            }

        return get_search_results_from_search(search)

    else:
        # Trying to get all articles so return only things that are published
        # for unauthenticated users
        search = None

        if authenticated:
            search = {}
        else:
            search = {"published" : True}

        return get_search_results_from_search(search)

    return None

def new():
    new_article = {}
    database.articles.insert(new_article)
    return Article(**new_article)

def save(article):
    print article._id
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

def delete(_id):
    try:
        database.articles.remove({"_id" : ObjectId(_id)})
        return True

    except Exception as e:
        print "Could not delete Article. Database Error:"
        print e

    return False

def read(_id):
    try:
        database.articles.update({ "_id" : ObjectId(_id) },{ "$inc": { "read_count" : 1 } }, True)
        return True
    except Exception as e:
        print "Could not read Article. Database Error:"
        print e

    return False

def love(_id):
    try:
        database.articles.update({ "_id" : ObjectId(_id) },{ "$inc": { "love_count" : 1 } }, True)
        return True
    except Exception as e:
        print "Could not love Article. Database Error:"
        print e

    return False
