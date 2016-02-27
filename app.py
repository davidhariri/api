from flask import Flask, request
from config import settings
from decorators import authenticate
import json

app = Flask(__name__)

@app.route("/")
@authenticate
def return_map(authenticated):
    if authenticated:
        return json.dumps({
            "message" : "Welcome back.",
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

if __name__ == "__main__":
	app.run(debug=settings["server"]["debug"], port=settings["server"]["port"])
