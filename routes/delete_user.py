from bottle import delete, response
import requests
import json

arango_url = "http://arangodb:8529/_db/_system/_api/cursor"
headers = {'content-type': 'application/json'}

@delete("/users/<key>")
def _(key):
    data = {
        "query": """
        FOR user IN users
        FILTER user._key == @key
        REMOVE user IN users
        RETURN OLD
        """,
        "bindVars": {"key": key}
    }

    try:
        arango_response = requests.post(arango_url, headers=headers, data=json.dumps(data))
        if arango_response.ok:
            return f"<template mix-target='[id=\"{key}\"]' mix-replace></template>"
        else:
            response.status = arango_response.status_code
            return f"<template mix-target='#message'>Failed to delete user: {arango_response.text}</template>"
    except requests.exceptions.RequestException as e:
        response.status = 500
        return f"<template mix-target='#message'>An error occurred: {e}</template>"
