"""
Use this script

COMMAND:
python3 update_xml_file.py 'http://localhost:8080/geoserver/gwc/rest/layers/' USERNAME PASSWORD ./layers.txt ./tile_layer_template.xml.txt

"""


import sys
import ast
import json
import requests
import xmltodict
from requests.auth import HTTPBasicAuth


URL = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
layer_file = sys.argv[4]
xml_file = sys.argv[5]


f = open(layer_file, "r")
layers = f.read()
layers_list = ast.literal_eval(layers)

for layer_name in layers_list:
    layerName = layer_name
    response = requests.get(
        URL + layerName + ".xml", auth=HTTPBasicAuth(username, password)
    )
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
