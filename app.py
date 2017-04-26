import os
from flask import Flask
from flask_restful import Api as API
import mongoengine

from routes import route_dict

# MARK - Setup Flask app
app = Flask(__name__)

# MARK - Setup Services
mongoengine.connect(
    host=os.environ.get("MONGODB_URI", "localhost:27017"),
    db="dhariri")

# Set up Flask-Restful API wrapper
api = API(app)

# MARK - Add routes from /routes/__init__.py
for route, resource in route_dict.items():
    api.add_resource(resource, route)

if __name__ == "__main__":
    # TODO: Make this an ENV var
    app.run(debug=os.environ.get("DEBUG", True))
