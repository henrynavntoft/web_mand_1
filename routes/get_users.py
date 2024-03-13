from bottle import get, template
import requests
import json

###############################
arango_url = "http://arangodb:8529/_db/_system/_api/cursor"
headers = {'content-type': 'application/json'}

@get("/")
def _():
    data = {"query": "FOR user IN users RETURN user"}
    try:
        arango_response = requests.post(arango_url, data=json.dumps(data), headers=headers)
        users_data = arango_response.json()
        return template('index', users=users_data['result'])
    except Exception as ex:
        print("Error in / route", str(ex))
    finally:
        pass
