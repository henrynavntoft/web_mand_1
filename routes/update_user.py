from bottle import post, request, response
import requests
import json

arango_url = "http://arangodb:8529/_db/_system/_api/cursor"
headers = {'content-type': 'application/json'}

@post("/update-user/<key>")
def update_user(key):
    user_first_name = request.forms.get("user_first_name")
    user_last_name = request.forms.get("user_last_name")

    data = {
        "query": """
        FOR user IN users
        FILTER user._key == @key
        UPDATE user WITH { user_first_name: @user_first_name, user_last_name: @user_last_name } IN users
        RETURN NEW
        """,
        "bindVars": {
            "key": key,
            "user_first_name": user_first_name,
            "user_last_name": user_last_name
        }
    }

    try:
        arango_response = requests.post(arango_url, headers=headers, data=json.dumps(data))
        if arango_response.ok:
            updated_user = arango_response.json()['result'][0]
            return f"<template mix-target='[id=\"user-{key}\"]'>{updated_user['user_first_name']} {updated_user['user_last_name']}</template>"
    except Exception as ex:
        return {"error": str(ex)}
    finally:
        pass