from flask import Flask, request
from config import settings
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
	return json.dumps({
        "message" : "Hi there! You are not authorized. If you'd like to know what endpoints you can use, please consult the endpoints array included in this dictionary. Further documentation is available at https://github.com/davidhariri/api",
        "endpoints" : ["/", "/articles/", "/articles/{id}"]
    }), 200

if __name__ == "__main__":
	app.run(debug=settings["debug"], port=settings["port"])
