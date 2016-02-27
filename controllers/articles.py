import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import datetime
from config import settings
import markdown

database = pymongo.MongoClient('mongodb://{}:{}{}'.format(settings["database"]["user"], settings["database"]["pass"], settings["database"]["url"]))["blog"]

def Article(article):
    article = json.loads(dumps(article))

    return {
        "id" : article["_id"]["$oid"],
        "key" : article["key"],
        "title" : article["title"],
        "content" : article["content"],
        "made" : article["made"]["$date"],
        "updated" : article["updated"]["$date"],
        "tags" : article["tags"],
        "published" : article["published"]
    }

def parse_articles(articles_from_db):
    articles = []

    for article in articles_from_db:
        articles.append(Article(article))

    return articles

def parse_content(markdown_content):
    html_content = markdown.markdown(markdown_content)

    return {
        "markdown" : markdown_content, # Raw markdown supported text
        "html" : html_content
    }

def find(key=None, tag=None, only_published=True):
    # Find by id (favoured over tag)
    if key != None:
        if only_published:
            return parse_articles(database.articles.find({"key" : key, "published" : True}).limit(1))
        else:
            return parse_articles(database.articles.find({"key" : key}).limit(1))

    # Find by tag
    if tag != None:
        if only_published:
            return parse_articles(database.articles.find({"tags" : tag, "published" : True}).limit(0))
        else:
            return parse_articles(database.articles.find({"tags" : tag}).limit(0))

    # Default response to find()
    if only_published:
        return parse_articles(database.articles.find({"published" : True}).sort("made", -1).limit(0))
    else:
        return parse_articles(database.articles.find().sort("made", -1).limit(0))

def new(key="", title="", content="", tags=None):
    now = datetime.datetime.utcnow()

    article = {
        "key" : key,
        "title" : title,
        "content" : parse_content(content),
        "tags" : tags,
        "updated" : now,
        "made" : now,
        "published" : False
    }

    article["id"] = database.articles.insert_one(article).inserted_id

    return Article(article)

def replace(article):
    database.articles.update(
        {
            "_id" : ObjectId(article["id"])
        },
        {
            "$set" : {
                "title" : article["title"],
                "key" : article["key"],
                "update" : datetime.datetime.utcnow(),
                "content" : parse_content(article["content"]["markdown"]),
                "published" : article["published"],
                "tags" : article["tags"]
            }
        },
        False
    )

    return article

def delete(id):
    database.articles.delete_one({"_id" : ObjectId(id)})

    return True
