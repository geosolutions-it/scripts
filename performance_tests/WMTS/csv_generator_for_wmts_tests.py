import os
import csv
import random
import requests
from lxml import etree as ET

#Layer properties inputs
wmts_getcap="wmts-getcapabilities.xml"

min_level = int(input("Please enter the minimun bound of the level:"))
max_level = int(input("Please enter the maximum bound of the level:"))
requests_count = int(input("Please enter the number of the Requests:"))
base_url = None
if not os.path.exists(wmts_getcap):
    base_url = input("Please enter the GeoServer URL (e.g. https://<your-server>/geoserver/gwc/service/wmts?):")
    url = base_url + "request=getcapabilities"
    r = requests.get(url, allow_redirects=True)
    open("wmts-getcapabilities.xml", "wb").write(r.content)
layer_name = input("Please enter the Layer Identifier:")
epsg = input("Please enter the EPSG (e.g. EPSG:4326):")
path = input("Please enter the Path of your workspace followed by the CSV filename:")

#Reading the GetCapabilities xml file  
#Check the name of the xml file that you have downloaded and if not the same replace it in the value of the $wmts_getcap parameter here below 

tree = ET.parse(wmts_getcap)
root = tree.getroot()
layers = tree.findall('{http://www.opengis.net/wmts/1.0}Contents/{http://www.opengis.net/wmts/1.0}Layer')

#Creating a dictionary from the layers data in the xml

tilematrixdict = {}

# The following 3 for loops are needed to parse the xml file pointing the layers first, then all its child tree such as the title, identifier, 
# tilematrixset until finding the tile matrix limit in order to extract the min tile row and col 
 

for layer in layers:
    title = layer.find("{http://www.opengis.net/ows/1.1}Title")
    identifier = layer.find("{http://www.opengis.net/ows/1.1}Identifier")
    tileMatrixSets = layer.findall("{http://www.opengis.net/wmts/1.0}TileMatrixSetLink/{http://www.opengis.net/wmts/1.0}TileMatrixSet")
    print("Layer Title: {}".format(title.text))
    _id = "{}".format(identifier.text)
    tilematrixdict[_id] = {}
    print("Layer Identifier: {}".format(_id))
    for tileMatrixSet in tileMatrixSets:
        _s = "{}".format(tileMatrixSet.text)
        tilematrixdict[_id][_s] = {}
        _l = ("{http://www.opengis.net/wmts/1.0}Contents/" + \
              "{http://www.opengis.net/wmts/1.0}Layer[{http://www.opengis.net/ows/1.1}Identifier = '" + _id + "']/" + \
              "{http://www.opengis.net/wmts/1.0}TileMatrixSetLink[{http://www.opengis.net/wmts/1.0}TileMatrixSet = '" + _s + "']/" + \
              "{http://www.opengis.net/wmts/1.0}TileMatrixSetLimits/" + \
              "{http://www.opengis.net/wmts/1.0}TileMatrixLimits")
        tileMatrixLimits = tree.findall(_l)
        for tileMatrixLimit in tileMatrixLimits:
            tileMatrix = tileMatrixLimit.find("{http://www.opengis.net/wmts/1.0}TileMatrix")
            _tm_id = int(tileMatrix.text.split(":")[-1:][0])
            minTileRow = tileMatrixLimit.find("{http://www.opengis.net/wmts/1.0}MinTileRow")
            maxTileRow = tileMatrixLimit.find("{http://www.opengis.net/wmts/1.0}MaxTileRow")
            minTileCol = tileMatrixLimit.find("{http://www.opengis.net/wmts/1.0}MinTileCol")
            maxTileCol = tileMatrixLimit.find("{http://www.opengis.net/wmts/1.0}MaxTileCol")
            tilematrixdict[_id][_s][_tm_id] = [float(minTileRow.text), float(maxTileRow.text), float(minTileCol.text), float(maxTileCol.text)]

			
#Writing a CSV file containing random levels requests  
			
myfile = open(path, 'w')

for i in range(1,requests_count + 1): 
    dict = tilematrixdict[layer_name][epsg]
    level = random.randint(min_level, max_level)
    row = random.randint(dict[level][0], dict[level][1])
    col = random.randint(dict[level][2], dict[level][3])
    myfile.write((str(level) + ";" + str(col) + ";" + str(row) + '\n')) 

myfile.close()
	
print(tilematrixdict)

#input("Press enter to exit")
