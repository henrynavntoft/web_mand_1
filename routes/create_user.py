from bottle import post, request, response, template
import requests
import json

arango_url = "http://arangodb:8529/_db/_system/_api/cursor"
headers = {'content-type': 'application/json'}

@post("/users")
def _():
    user_first_name = request.forms.get("user_first_name")
    user_last_name = request.forms.get("user_last_name")

    data = {
        "query": """
        INSERT { user_first_name: @user_first_name, user_last_name: @user_last_name } 
        INTO users
        RETURN NEW
        """,
        "bindVars": {
            "user_first_name": user_first_name,
            "user_last_name": user_last_name
        }
    }

    try:
        arango_response = requests.post(arango_url, headers=headers, data=json.dumps(data))
        if arango_response.ok:
            new_user = arango_response.json()['result'][0]
        # Use the user_entry template to generate HTML for the new user
            new_user_html = template('_user.html', user=new_user)
            return f"<template mix-target='#users' mix-top>{new_user_html}</template>"
        else:
            response.status = arango_response.status_code
            return f"Failed to create user: {arango_response.text}"
    except requests.exceptions.RequestException as e:
        response.status = 500
        return f"An error occurred: {e}"
