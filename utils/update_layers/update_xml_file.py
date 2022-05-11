"""
Use this script

COMMAND:
python3 update_xml_file.py 'http://localhost:8080/geoserver/gwc/rest/layers/' USERNAME PASSWORD ./layers.txt ./tile_layer_template.xml.txt

System Argument needs to pass:
USERNAME
PASSWORD
LAYERS FILE
XML FILE

"""


import sys
import ast
import json
import requests
import xmltodict
from requests.auth import HTTPBasicAuth


if len(sys.argv) > 6 or len(sys.argv) < 6:
    raise Exception("Expected 6 arguments are not given.")

URL = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
layer_file = sys.argv[4]
xml_file = sys.argv[5]

if not (username and password and layer_file and xml_file):
    raise Exception(
        "System Argument needs to pass: (USERNAME, PASSWORD, LAYERS FILE, XML FILE)"
    )
elif ".xml" not in xml_file:
    raise Exception("Please pass xml file here.")
elif ".txt" not in layer_file:
    raise Exception("Please pass txt file for layers.")
elif "layers" not in URL:
    raise Exception("Please pass correct layer URL.")

f = open(layer_file, "r")
layers = f.read()
layers_list = ast.literal_eval(layers)

for layer_name in layers_list:
    layerName = layer_name
    response = requests.get(
        URL + layerName + ".xml", auth=HTTPBasicAuth(username, password)
    )

    if response.status_code == 401:
        raise Exception("Incorrect USERNAME or PASSWORD")

    xpars = xmltodict.parse(response.text)

    layerId = xpars["GeoServerLayer"]["id"]

    f = open(xml_file, "r")
    data = f.read()

    file = xmltodict.parse(data)
    file["GeoServerLayer"]["id"] = layerId
    file["GeoServerLayer"]["name"] = layerName

    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "PUT",
        URL + layerName,
        headers=headers,
        data=json.dumps(file),
        auth=HTTPBasicAuth(username, password),
    )

    print(response.text)
