import sys
import requests

import config

HEADERS = {
        "Content-Type": "application/json",
        "Authorization": config.HTTP_BASIC_AUTH,
        "Cache-Control": "no-cache",
        "appKey": config.APP_KEY
        }

def putDataToThing(thingName, propertyName, data):
    url = "http://{}/Thingworx/Things/{}/Properties/{}".format(config.THINGWORX_HOST, thingName, propertyName)
    payload = str("{\"" + propertyName + "\":" + str(data) + "}")
    response = requests.request("PUT", url, data=payload, headers=HEADERS)
    print(url + "--" + str(response.status_code))
    return response.status_code


def createThing(thingName):
    url = "http://{}/Thingworx/Resources/EntityServices/Services/CreateThing".format(config.THINGWORX_HOST)
    payload = str("{\"name\":" + "\"" + thingName + "\",\"thingTemplateName\": \"RemoteThing\"}")
    response = requests.request("POST", url, data=payload, headers=HEADERS)
    print(url + "--" + str(response.status_code))
    return response.status_code

def getNamesOfThings():
    url = "http://{}/Thingworx/Things".format(config.THINGWORX_HOST)
    response = requests.request("GET", url, headers=HEADERS)
    print(url + "--" + str(response.status_code))
    return response.status_code
