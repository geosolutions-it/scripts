import csv
import random
from lxml import etree as ET

#Layer properties inputs

min_level = int(input("Please enter the minimun bound of the level:  "))
max_level = int(input("Please enter the maximum bound of the level:  "))
requests = int(input("Please enter the number of the Requests:  "))
layer_name = input("Please enter the Layer Identifier in quotes:  ")
epsg = input("Please enter the EPSG (e.g. 'EPSG:4326'):  ")

myfile = open('C:\Path', 'w')

#Reading the GetCapabilities xml file  

wmts_getcap="wmts-getcapabilities.xml"
tree = ET.parse(wmts_getcap)
root = tree.getroot()
layers = tree.findall('{http://www.opengis.net/wmts/1.0}Contents/{http://www.opengis.net/wmts/1.0}Layer')

#Creating a dictionary from the layers data in the xml

tilematrixdict = {}
for layer in layers:
    title = layer.find("{http://www.opengis.net/ows/1.1}Title")
    identifier = layer.find("{http://www.opengis.net/ows/1.1}Identifier")
    tileMatrixSets = layer.findall("{http://www.opengis.net/wmts/1.0}TileMatrixSetLink/{http://www.opengis.net/wmts/1.0}TileMatrixSet")
    print "Layer Title: {}".format(title.text)
    _id = "{}".format(identifier.text)
    tilematrixdict[_id] = {}
    print "Layer Identifier: {}".format(_id)
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
			
myfile = open('C:\Path', 'w')

for i in range(1,requests + 1): 
    dict = tilematrixdict[layer_name][epsg]
    level = random.randint(min_level, max_level)
    row = random.randint(dict[level][0], dict[level][1])
    col = random.randint(dict[level][2], dict[level][3])
    myfile.write((str(level) + ";" + str(col) + ";" + str(row) + '\n')) 
	
print tilematrixdict

input("Press enter to exit")
