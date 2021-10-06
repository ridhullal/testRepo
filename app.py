from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

import requests as core_requests

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = make_openweathermap_request(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def make_openweathermap_request(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    print('https://api.openweathermap.org/data/2.5/weather?q={}&appid=4caf7420789e9f763a81fbc58dc34e31'.format(city))

    try:
        r = core_requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid=4caf7420789e9f763a81fbc58dc34e31'.format(city))
        current_temp = r.json()['main']['temp']
        current_temp = float(current_temp) - 273.0
        current_temp = int(current_temp)

        speech_response = 'Current temperature in {} is {} Celsius'.format(city, current_temp)
    except Exception as e:
        speech_response = 'Unable to get temperature of {}'.format(city)

    return {
        "fulfillmentText": speech_response,
        "source": "Yahoo Weather"
    }



if __name__ == '__main__':
    app.run(debug=True, port=5000)
