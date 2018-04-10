import json
import requests

HEADERS = {
        "Content-Type": "application/json",
        "Authorization": config.HTTP_BASIC_AUTH,
        "Cache-Control": "no-cache",
        "appKey": config.APP_KEY
        }

def putDataToThing(thing_name, property_name, data, config):
    url = "http://{}/Thingworx/Things/{}/Properties/{}".format(config["thingworx_host"], thing_name, property_name)
    payload = str("{\"" + property_name + "\":" + str(data) + "}")
    print(payload)
    response = requests.request("PUT", url, data=payload, headers=HEADERS)
    print(url + "--" + str(response.status_code))
    return response.status_code


def enableThing(thing_name, config):
    url = "http://{}/Thingworx/Things/{}/Services/EnableThing".format(config["thingworx_host"], thing_name)
    response = requests.request("PUT", url, headers=HEADERS)
    print(response.status_code)
    return response.status_code

def createThing(thing_name, config):
    url = "http://{}/Thingworx/Resources/EntityServices/Services/CreateThing".format(config["thingworx_host"])
    payload = str("{\"name\":" + "\"" + thing_name + "\",\"thingTemplateName\": \"RemoteThing\"}")
    print(payload)
    response = requests.request("POST", url, data=payload, headers=HEADERS)
    print(url + "--" + str(response.status_code))
    enableThing(thing_name, config)
    return response.status_code


def addPropertyToThing(thing_name, property_name, property_type, config):
    url = "http://{}/Thingworx/Things/{}/Services/AddPropertyDefinition".format(config["thingworx_host"], thing_name)
    payload = str("{\"name\":" + "\"" + property_name + "\",\"type\":\"" + property_type + "\"}")
    response = requests.request("POST", url, data=payload, headers=HEADERS)
    print(url + "--" + str(response.status_code))
    return response.status_code


def getNamesOfThings(config):
    url = "http://{}/Thingworx/Things".format(config["thingworx_host"])
    temp_headers = HEADERS
    temp_headers["Accept"] = "application/json"
    response = requests.request("GET", url, headers=temp_headers)
    print(url + "--" + str(response.status_code))

    # Convert response to array of names
    names = []
    print(response.text)
    data = json.loads(response.text)
    for thing in data["rows"]:
        names.append(thing["name"])
    return names
