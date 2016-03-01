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

# Check articles endpoints
auth_articles_req = requests.get(base_url+"articles/", auth=auth_user)
evaluate(
    "All articles with authentication",
    auth_articles_req.status_code == 200
)

articles_req = requests.get(base_url+"articles/")
evaluate(
    "All articles with no authentication",
    articles_req.status_code == 200
)

create_article_req = requests.post(base_url+"articles/")
evaluate(
    "Creating article with no authentication",
    create_article_req.status_code == 401
)

auth_create_article_req = requests.post(base_url+"articles/", auth=auth_user)
evaluate(
    "Creating article with authentication",
    auth_create_article_req.status_code == 201
)

new_article = auth_create_article_req.json()

# Check article endpoints
# Edit the new_article
new_article["content"]["markdown"] = "# A test\n\nHello World"
new_article_edit_req = requests.put(base_url+"articles/"+new_article["_id"]["$oid"], json=new_article)
evaluate(
    "Editing an article without authentication",
    new_article_edit_req.status_code == 401
)

new_article["content"]["markdown"] = "# A test\n\nHello World"
new_article_edit_req_auth = requests.put(base_url+"articles/"+new_article["_id"]["$oid"], auth=auth_user, json=new_article)
evaluate(
    "Editing an article with authentication",
    new_article_edit_req_auth.status_code == 200
)

print new_article_edit_req_auth.json()

new_article_delete_req = requests.delete(base_url+"articles/"+new_article["_id"]["$oid"], auth=auth_user)
evaluate(
    "Deleting an article without authentication",
    new_article_edit_req.status_code == 401
)

new_article_delete_req_auth = requests.delete(base_url+"articles/"+new_article["_id"]["$oid"], auth=auth_user)
evaluate(
    "Deleting an article with authentication",
    new_article_edit_req_auth.status_code == 200
)
