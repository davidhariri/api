from flask import Flask, request
from controllers import articles as Articles
from config import settings
from decorators import authenticate
from flask.ext.cors import CORS
from json import loads
from bson.json_util import dumps

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
			return dumps(Articles.new().__dict__), 201
		else:
			return dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

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
			print Articles.delete(_id)
			return dumps({
				"message" : "Deleted {}".format(_id)
			}), 200
		else:
			return dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

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
