from flask import Flask, request
from controllers import articles as Articles
from config import settings
from decorators import authenticate
from flask.ext.cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
@authenticate
def return_welcome(authenticated):
	if authenticated:
		return json.dumps({
			"message" : "Welcome back!",
			"authenticated" : True
		}), 200
	elif authenticated == None:
		return json.dumps({
			"message" : "Hi there! You are not authorized. If you'd like to know what endpoints you can use, please consult the documentation available at https://github.com/davidhariri/api",
			"authenticated" : False
		}), 200
	else:
		return json.dumps({
			"message" : "Your authentication was unacceptable.",
			"authenticated" : False
		}), 401

@app.route("/articles/", methods=["GET", "POST"])
@authenticate
def return_articles(authenticated):
	if request.method == "GET":
		if authenticated:
			# Will return all articles
			return json.dumps(Articles.find(only_published=False)), 200
		else:
			# Will return, by default, only published articles
			return json.dumps(Articles.find()), 200
	elif request.method == "POST":
		if authenticated:
			return json.dumps(Articles.new(
				key=request.form.get("key") if request.form.get("key") != None else "",
				title=request.form.get("title") if request.form.get("title") != None else "",
				content=request.form.get("content") if request.form.get("content") != None else "",
				tags=request.form.get("tags")
			)), 201
		else:
			return json.dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

@app.route("/articles/<url>", methods=["GET", "PUT", "DELETE"])
@authenticate
def return_article(url, authenticated):
	if request.method == "GET":
		results = []

		if authenticated:
			results = Articles.find(key=url, only_published=False)
		else:
			results = Articles.find(key=url)

		if len(results) > 0:
			return json.dumps(results[0]), 200
		else:
			return json.dumps({"message" : "Article not found."}), 404

	elif request.method == "PUT":
		if authenticated:
			Articles.replace(request.json)
			return json.dumps({"message" : "Replaced article"}), 200
		else:
			return json.dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

	elif request.method == "DELETE":
		if authenticated:
			return json.dumps(Articles.delete(url)), 200
		else:
			return json.dumps({
				"message" : "This method is only allowed for administrators."
			}), 401

@app.errorhandler(404)
def return_404(e):
	return json.dumps({
		"message" : "That resource doesn't exist"
	}), 404

@app.errorhandler(405)
def return_405(e):
	return json.dumps({
		"message" : "That method is not allowed"
	}), 405

@app.errorhandler(500)
def return_500(e):
	return json.dumps({
		"message" : "Internal server error. Please report issues here: https://github.com/davidhariri/api/issues"
	}), 500

if __name__ == "__main__":
	app.run(debug=settings["server"]["debug"], port=settings["server"]["port"])
