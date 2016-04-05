import pymongo
import json
import requests

from datetime import datetime
from config import settings
from controllers import pings as Pings

database = pymongo.MongoClient('mongodb://{}:{}{}'.format(settings["database"]["user"], settings["database"]["pass"], settings["database"]["url"]))["blog"]

special_locations = {
    "43.660,-79.329" : "at work",
    "43.667,-79.340" : "at home"
}

class GeneralLocation(object):
    def __init__(self, ping):

        def round_and_pad(float_num):
            return format(round(float_num, 3), '.3f')

        self.lon = round_and_pad(ping.location['x'])
        self.lat = round_and_pad(ping.location['y'])

def get():
    ping = Pings.find(1)[0]
    gnrl_loc = GeneralLocation(ping)

    ulid = "{},{}".format(gnrl_loc.lat, gnrl_loc.lon)
    loc_str = None
    act_str = ""

    # See if we're in a special location
    try:
        loc_str = special_locations[ulid]
    except:
        pass

    speed = ping.location['speed']

    # See if we're doing any activities
    if(speed >= 1.4):
        act_str = "walking "
    elif(speed >= 3.2):
        act_str = "running "
    elif(speed >= 12.0):
        act_str = "travelling "

    if not loc_str:
        # Let's try and get the city of where we are from Google:
        place_response = requests.get("http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=true".format(ping.location['y'], ping.location['x']))
        places = place_response.json()

        for component in places["results"][0]["address_components"]:
            if "locality" in component["types"] or "neighborhood" in component["types"]:
                loc_str = "in {}".format(component["long_name"])
                break

    return {
        "text" : "I'm {}{}".format(act_str, loc_str),
        "location" : gnrl_loc.__dict__,
        "date" : ping.time
    }
