# -*- coding: utf-8 -*-
import requests
from config import settings

def evaluate(description, assertion, log=None):
    result = "\033[91mFailed ✘"

    if assertion:
        result = "\033[92mPassed ✔"

    print "\033[1m{}\033[0m => {}\033[0m".format(description, result)

base_url = "{}:{}/".format(settings["server"]["url"], settings["server"]["port"])
auth_user = (settings["authentication"]["email"], settings["authentication"]["pass"])
# Check authorization
unauth_req = requests.get(base_url)
evaluate(
    "Request with no authentication",
    unauth_req.status_code == 200 and unauth_req.json()["authenticated"] == False
)

bad_auth_req = requests.get(base_url, auth=("no", "good"))
evaluate(
    "Request with bad authentication",
    bad_auth_req.status_code == 401 and bad_auth_req.json()["authenticated"] == False
)

auth_req = requests.get(base_url, auth=auth_user)
evaluate(
    "Request with authentication",
    auth_req.status_code == 200 and auth_req.json()["authenticated"] == True
)
