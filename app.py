from flask import Flask, request
from config import settings
from decorators import authenticate
from flask.ext.cors import CORS
from json import loads
from bson.json_util import dumps
import uuid

from controllers import articles as Articles
from controllers import pings as Pings

app = Flask(__name__)
CORS(app)

@app.route("/")
@authenticate
def return_welcome(authenticated):
	if authenticated:
		return dumps({
			"message" : "Welcome back!",
			"authenticated" : True
		}), 200
	elif authenticated == None:
		return dumps({
			"message" : "Hi there! You are not authorized. If you'd like to know what endpoints you can use, please consult the documentation available at https://github.com/davidhariri/api",
			"authenticated" : False
		}), 200
	else:
		return dumps({
			"message" : "Your authentication was unacceptable.",
			"authenticated" : False
		}), 401

@app.route("/articles/", methods=["GET", "POST"])
@authenticate
def return_articles(authenticated):
	if request.method == "GET":
		# Will return all articles
		results = []

		for article in Articles.find(authenticated=authenticated):
			results.append(article.__dict__)

		return dumps(results), 200

	elif request.method == "POST":
		if authenticated:
			new_article = Articles.new()
			return dumps(new_article.__dict__), 201
		else:
			return dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

# These endpoints uses a GET method because it's easier to deal with for the client
# TODO: This would be a good place to put a rate limiter in the future...
@app.route("/articles/<_id>/read", methods=["GET", "PUT", "POST"])
def read_article(_id):
	if Articles.read(_id):
		return dumps({
			"message" : "Read article {}".format(_id)
		}), 200
	else:
		return dumps({
			"message" : "Article could not be read"
		}), 400

@app.route("/articles/<_id>/love", methods=["GET", "PUT", "POST"])
def love_article(_id):
	if Articles.love(_id):
		return dumps({
			"message" : "Loved article {}".format(_id)
		}), 200
	else:
		return dumps({
			"message" : "Article could not be loved"
		}), 400

@app.route("/articles/<_id>", methods=["GET", "PUT", "DELETE"])
@authenticate
def return_article(_id, authenticated):
	if request.method == "GET":
		results = []

		for article in Articles.find(_id=_id, authenticated=authenticated):
			results.append(article.__dict__)

		if len(results) > 0:
			return dumps(results[0]), 200
		else:
			return dumps({"message" : "Article not found."}), 404

	elif request.method == "PUT":
		if authenticated:
			article_data = loads(request.data)
			article = Articles.Article(**article_data)
			article.render_html()
			saved = Articles.save(article)

			if saved:
				return dumps(saved.__dict__), 200
			else:
				return dumps({
					"message" : "Object could not be saved"
				}), 400
		else:
			return dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

	elif request.method == "DELETE":
		if authenticated:
			if Articles.delete(_id):
				return dumps({
					"message" : "Deleted article {}".format(_id)
				}), 200
			else:
				return dumps({
					"message" : "Article could not be deleted"
				}), 400
		else:
			return dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

@app.route("/images/", methods=["POST"])
@authenticate
def upload_return_url(authenticated):
	if authenticated:
		file = request.files["file"]
		file_extension = file.filename.split(".")[-1]
		file_name = "{}.{}".format(uuid.uuid4(), file_extension)

		if file_extension in set(["png", "jpg", "jpeg", "gif", "svg"]):
			file.save("images/{}".format(file_name))

			return dumps({
				"url" : "https://images.dhariri.com/{}".format(file_name)
			}), 201
		else:
			return dumps({
				"message" : "No good"
			}), 400
	else:
		return dumps({
			"message" : "This method is only allowed for administrators."
		}), 401

@app.route("/ping/", methods=["POST"])
@authenticate
def accept_ping(authenticated):
	data = loads(request.data)

	if authenticated:
		if "locations" in data and isinstance(data["locations"], list):
			for location_object in data["locations"]:
				ping = Pings.Ping(**location_object)
				ping.save()

			return dumps({
				"message" : "Got it"
			}), 201
		else:
			return dumps({
				"message" : "No good"
			}), 400
	else:
		return dumps({
			"message" : "This method is only allowed for administrators."
		}), 401

@app.route("/ping/recent/", methods=["GET"])
def return_recent_locations():
	# Return all the pings visited recently
	results = []

	for ping in Pings.find():
		results.append(ping.__dict__)

	return dumps(results), 200

# Error handlers:
@app.errorhandler(404)
def return_404(e):
	return dumps({
		"message" : "That resource doesn't exist"
	}), 404

@app.errorhandler(405)
def return_405(e):
	return dumps({
		"message" : "That method is not allowed"
	}), 405

@app.errorhandler(500)
def return_500(e):
	return dumps({
		"message" : "Internal server error. Please report issues here: https://github.com/davidhariri/api/issues"
	}), 500

@app.errorhandler(400)
def return_500(e):
	return dumps({
		"message" : "Bad request."
	}), 400

if __name__ == "__main__":
	app.run(debug=settings["server"]["debug"], port=settings["server"]["port"])
