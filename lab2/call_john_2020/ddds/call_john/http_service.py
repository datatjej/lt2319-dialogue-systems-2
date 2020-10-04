# -*- coding: utf-8 -*-

import json

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)


environment.filters["json"] = jsonfilter

with open('call_john/contacts.json', "r") as json_file:
    PHONEBOOK = json.load(json_file)

PHONEBOOK["contact_john"]["mobile"] = "0701234567"
PHONEBOOK["contact_john"]["work"] = "0736582934"
PHONEBOOK["contact_john"]["home"] = "031122363"
PHONEBOOK["contact_mary"]["mobile"] = "0706574839"
PHONEBOOK["contact_mary"]["work"] = "0784736475"
PHONEBOOK["contact_mary"]["home"] = "031847528"
with open('call_john/contacts.json', "w") as json_file:
    json.dump(PHONEBOOK, json_file)
	
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
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
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
    payload = response_template.render(value=value,
                                       grammar_entry=grammar_entry)
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
    return response


def multiple_query_response(results):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
        {% for result in results %}
          {
            "value": {{result.value|json}},
            "confidence": 1.0,
            "grammar_entry": {{result.grammar_entry|json}}
          }{{"," if not loop.last}}
        {% endfor %}
        ]
      }
    }
     """)
    payload = response_template.render(results=results)
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
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
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
    response = app.response_class(response=payload,
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route("/make_call", methods=['POST'])
def make_call():
    payload = request.get_json()
    contact_to_call = payload["context"]["facts"]["contact_to_call"]["value"]
    number_type_to_call = payload["context"]["facts"]["number_type_to_call"]["value"]
    phone_number_of_contact = PHONEBOOK[contact_to_call][number_type_to_call]
    print(PHONEBOOK)
    with open('call_john/contacts.json', "w") as json_file:
        json.dump(PHONEBOOK, json_file)
    return action_success_response()
	
#@app.route("/phone_number_of_contact", methods=['POST'])
#def phone_number_of_contact():
#    phone_number_of_contact = PHONEBOOK["contact_to_call"]["number_type_to_call"]
#    return query_response(value=phone_number_of_contact, grammar_entry=None)
	
