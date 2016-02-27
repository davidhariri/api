# API
Welcome! This is the public documentation for the API that drives my online presence at [dhariri.com](https://dhariri.com). Read on (or visit [api.dhariri.com](https://api.dhariri.com) to find out what access you have to my data!

## Installation
You can install everything you need to get started developing the API with [pip](https://pip.pypa.io/en/stable/installing/) and the following command:
```
sudo pip install -r requirements.txt
```
You will, however, need a configuration file (`/config.py`). They look like this:
```python
settings = {
    "database" : {
        "url" : "", # expects a mongo instance url
        "user" : "", # a username
        "pass" : "", # a password
    },
    "authentication" : {
        "email" : "", # expects a string to be used in your auth headers before the colon
        "pass" : "" # expects a string to be used in your auth headers after the colon
    },
    "server" : {
        "url" : "http://localhost",
        "debug" : True,
        "port" : 8000
    }
}
```

## Tests
To keep things sane, I've made a simple file where all tests of endpoints are made. If you'd like to contribute to this repository, don't forget to test your work before opening a pull request :relaxed:

## Authorization
To keep things simple, all authorization happens with a username and password over SSL as a Basic Authentication header. Insecure requests to the API will be ignored.
```
curl -u an@email.com:notarealpassword https://api.dhariri.com
```

## Response Codes
These are all the valid endpoints you can access with our API. We use standard HTTP codes in our responses to notify you of how things went with your requests. **20x codes are good things and 40x or 50x codes mean bad things**.

Code | Description
--- | ---
**200** | Your `GET` request was successful and the resource was returned to you. Your `POST` request was successful and the modified resource was returned to you. Your `DELETE` operation was successful.
**201** | Your `POST` request was successful and a new resource was returned to you.
**400** | Your request was malformed and could not be executed.
**401** | Your request did not include a proper authentication header.
**404** | We couldn't find the resource you requested.
**403** | You included an authorization header, but you're not authorized to access the requested resource.
**405** | You're accessing an endpoint with a method that isn't supported.
**500** | Your request made our server explode :fire:. Report it here in issues!

## Endpoints

### /
Method | Auth? | Description | Response
--- | --- | --- | ---
**GET** | Optional | Test your API access. Gets a list of valid endpoints you can access | `200, [...]`

### /articles/
Method | Auth? | Description | Response
--- | --- | --- | ---
**GET** | Optional | Retrieve all the published articles I've made. If authorized, this will return unpublished articles as well. | `200, [{...}]`
**POST** | Needed | Makes a new article. Accepts parameters, but none are required. | `201, [{...}]`

### /articles/{url_key}
Method | Auth? | Description | Response
--- | --- | --- | ---
**GET** | Optional | Will only return a published article unless authorized. | `200, {...}`
**PUT** | Needed | Replaces an article. For obvious reasons, authentication is required. | `200, {...}`

### /articles/shared/{oid}
Method | Auth? | Description | Response
--- | --- | --- | ---
**GET** | Optional | Will return an article, published or unpublished without authorization | `200, {...}`
