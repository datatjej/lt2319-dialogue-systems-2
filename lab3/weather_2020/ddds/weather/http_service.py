# -*- coding: utf-8 -*-

import json

from flask import Flask, request
from jinja2 import Environment
from urllib.request import Request, urlopen

app = Flask(__name__)
environment = Environment()

def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter

def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)
    payload = response_template.render(message=message)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": {{value|json}},
            "confidence": 1.0,
            "grammar_entry": {{grammar_entry|json}}
          }
        ]
      }
    }
    """)
    payload = response_template.render(value=value, grammar_entry=grammar_entry)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def validator_response(is_valid):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "is_valid": {{is_valid|json}}
      }
    }
    """)
    payload = response_template.render(is_valid=is_valid)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": "dummy",
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/action_success_response", methods=['POST'])
def action_success_response():
    response_template = environment.from_string("""
   {
     "status": "success",
     "data": {
       "version": "1.1"
     }
   }
   """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response

def get_data(city, country, unit, key="55499e7f852813ee179f2dad9bf2e3c6"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={unit}&APPID={key}"
    print(url)
    request = Request(url)
    response = urlopen(request)
    data = response.read()
    return json.loads(data)

@app.route("/temperature", methods=['POST'])
def temperature():
    payload = request.get_json()
    city = payload["context"]["facts"]["city_to_search"]["grammar_entry"]
    country = payload["context"]["facts"]["country_to_search"]["value"]
    unit = "metric"
    if "selected_unit" in payload['context']['facts'].keys():
        selected_unit = payload["context"]["facts"]["selected_unit"]["grammar_entry"]
        print("UNIT IN SELECTED_UNIT: ", selected_unit)
        if selected_unit.lower() == "kelvin":
            unit = "standard"
        elif selected_unit.lower() == "fahrenheit":
            unit = "imperial"
    print("unit: ", unit)
    data = get_data(city, country, unit)
    temp = data['main']['temp']
    tempstr = str(temp)
    print(tempstr) 
    return query_response(value=tempstr, grammar_entry=None)
	
@app.route("/weather", methods=['POST'])
def weather():
    payload = request.get_json()
    city = payload["context"]["facts"]["city_to_search"]["grammar_entry"]
    country = payload["context"]["facts"]["country_to_search"]["grammar_entry"]
    data = get_data(city, country, unit="metric")
    weather = data["weather"][0]["description"]
    weather = str(weather)
    print(weather)
    return query_response(value=weather, grammar_entry=None)