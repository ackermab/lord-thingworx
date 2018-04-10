import json
import requests

HEADERS = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }

def putDataToThing(thing_name, property_name, data, config):
    headers = HEADERS
    headers["http_basic_auth"] = config["http_basic_auth"]
    headers["appKey"] = config["app_key"]
    url = "http://{}/Thingworx/Things/{}/Properties/{}".format(config["thingworx_host"], thing_name, property_name)
    payload = str("{\"" + property_name + "\":" + str(data) + "}")
    print(payload)
    response = requests.request("PUT", url, data=payload, headers=headers)
    print(url + "--" + str(response.status_code))
    return response.status_code


def enableThing(thing_name, config):
    headers = HEADERS
    headers["http_basic_auth"] = config["http_basic_auth"]
    headers["appKey"] = config["app_key"]
    url = "http://{}/Thingworx/Things/{}/Services/EnableThing".format(config["thingworx_host"], thing_name)
    response = requests.request("PUT", url, headers=headers)
    print(response.status_code)
    return response.status_code

def createThing(thing_name, config):
    headers = HEADERS
    headers["http_basic_auth"] = config["http_basic_auth"]
    headers["appKey"] = config["app_key"]
    url = "http://{}/Thingworx/Resources/EntityServices/Services/CreateThing".format(config["thingworx_host"])
    payload = str("{\"name\":" + "\"" + thing_name + "\",\"thingTemplateName\": \"RemoteThing\"}")
    print(payload)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(url + "--" + str(response.status_code))
    enableThing(thing_name, config)
    return response.status_code


def addPropertyToThing(thing_name, property_name, property_type, config):
    headers = HEADERS
    headers["http_basic_auth"] = config["http_basic_auth"]
    headers["appKey"] = config["app_key"]
    url = "http://{}/Thingworx/Things/{}/Services/AddPropertyDefinition".format(config["thingworx_host"], thing_name)
    payload = str("{\"name\":" + "\"" + property_name + "\",\"type\":\"" + property_type + "\"}")
    response = requests.request("POST", url, data=payload, headers=headers)
    print(url + "--" + str(response.status_code))
    return response.status_code


def getNamesOfThings(config):
    headers = HEADERS
    headers["http_basic_auth"] = config["http_basic_auth"]
    headers["appKey"] = config["app_key"]
    url = "http://{}/Thingworx/Things".format(config["thingworx_host"])
    headers["Accept"] = "application/json"
    response = requests.request("GET", url, headers=headers)
    print(url + "--" + str(response.status_code))

    # Convert response to array of names
    names = []
    print(response.text)
    data = json.loads(response.text)
    for thing in data["rows"]:
        names.append(thing["name"])
    return names
