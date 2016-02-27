import requests
from config import settings

def evaluate(description, assertion):
    result = "\033[91mFailed ✘"

    if assertion:
        result = "\033[92mPassed ✔"

    print "\033[1m{}\033[0m => {}\033[0m".format(description, result)
