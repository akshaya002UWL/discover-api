import random
import re
from typing import Dict, List
import uuid
from flask import Flask, request, render_template, send_file, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from enum import Enum
import threading
import json
import requests



UPLOAD_FOLDER = 'templates'
ALLOWED_EXTENSIONS = set(['json'])
app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb://admin:admin@adapt-mongo-adapt.cp4ba-mission-16bf47a9dc965a843455de9f2aef2035-0000.eu-de.containers.appdomain.cloud:32535/LTI?authSource=admin'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

@app.route('/api/swagger.json')
def swagger_json():
    # Read before use: http://flask.pocoo.org/docs/0.12/api/#flask.send_file
    return send_file('swagger.json')


SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={  # Swagger UI config overrides
    'app_name': "Add/update JD"
},)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@app.get('/common-assets')
def commonassets():
    url = "https://cpd-ibm-cloudpaks.cp4ba-mission-16bf47a9dc965a843455de9f2aef2035-0000.eu-de.containers.appdomain.cloud/bas/dba/studio/platform/common-assets"
    payload={}
    headers = {
    'Authorization': 'Basic Y2VhZG1pbjpjZWFkbWluMTIz'
    }
    response = requests.request("GET", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/detail')
def detail():
    id = request.args.get("id")
    url = "https://cpd-ibm-cloudpaks.cp4ba-mission-16bf47a9dc965a843455de9f2aef2035-0000.eu-de.containers.appdomain.cloud/bas/dba/studio/platform/common-assets/<id>/versions?optional_parts=operations%2Corigin"
    getURL = url.replace("<id>", id)
    print(getURL)
    payload={}
    headers = {
    'Authorization': 'Basic Y2VhZG1pbjpjZWFkbWluMTIz'
    }
    response = requests.request("GET", getURL, headers=headers, data=payload,verify=False)
    return (response.text)

@app.route('/auth', methods=['POST'])
def auth():
    input = request.get_json()
    url = "https://account.uipath.com/oauth/token"
    payload = json.dumps({
    "grant_type": "refresh_token",
    "client_id": input["client_id"],
    "refresh_token": input["refresh_token"],
    })
    headers = {
    'Content-Type': 'application/json'    }
    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/folders')
def folders():
    url = "https://cloud.uipath.com/ibmiruyvjn/TestAutomation/orchestrator_/odata/folders"

    headers = {
    'Authorization': 'Bearer '+request.headers.get('Authorization')
    }
    payload={}

    response = requests.request("GET", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/Releases')
def Releases():
    url = "https://cloud.uipath.com/ibmiruyvjn/TestAutomation/odata/Releases"
    release_id = request.args.get("release")
    payload={}
    headers = {
    'X-UIPATH-OrganizationUnitId': release_id,
    'Authorization': 'Bearer '+request.headers.get('Authorization')
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return (response.text)

@app.post('/StartProcess')
def StartProcess():
    input = request.get_json()

    url = "https://cloud.uipath.com/ibmiruyvjn/TestAutomation/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"

    payload = json.dumps({
    "startInfo": {
        "ReleaseKey": input["key"],
        "Strategy": "ModernJobsCount",
        "JobsCount": 1,
        "InputArguments": "{}"
    }
    })
    print(payload)
    headers = {
    'Content-Type': 'application/json',
    'X-UIPATH-OrganizationUnitId': input['folder_id'],
    'Authorization': 'Bearer '+request.headers.get('Authorization')
    }
    print(headers)
    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/openapi')
def openapi():
    name = request.args.get("name")
    project_name = request.args.get("project_name")

    url = "https://cpd-ibm-cloudpaks.cp4ba-mission-16bf47a9dc965a843455de9f2aef2035-0000.eu-de.containers.appdomain.cloud/bawaut/automationservices/rest/<project_name>/<name>/docs"
    reeplace_projectName = url.replace("<project_name>",project_name)
    replace_name = reeplace_projectName.replace("<name>",name)

    payload={}
    headers = {
    'Authorization': 'Basic Y2VhZG1pbjpjZWFkbWluMTIz'
    
    }
    print(replace_name)
    response = requests.request("GET", replace_name, headers=headers, data=payload,verify=False)
    return (response.text)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)