#!/usr/bin/env python

import string
import sys
import os
from os import listdir
from os.path import isfile, join
#remove if not needed
from xml.dom import minidom
import xml.etree.ElementTree as ET
# =============================================================================
# Consts
# =============================================================================
separator = ';'


# =============================================================================
def Usage():
    print 'Usage: time_request.py -capabilities_doc capabilities.xml -layer layer [-verbose] -name'
    sys.exit(1)

# =============================================================================

#def printOut(bbox):
#  print '%s,%s,%s,%s' \
#                    % ('{0:.{1}f}'.format(bbox[0],6),'{0:.{1}f}'.format(bbox[1],6),'{0:.{1}f}'.format(bbox[2],6),'{0:.{1}f}'.format(bbox[3],6))

def printOut(layer,time):
  print layer + separator + time

def getLayer(root,layerName):
  return root.find(".//{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer/{http://www.opengis.net/wms}Layer/[{http://www.opengis.net/wms}Name='"+ layerName +"']")
    
def getDimensions(layer):
  return root.find(".//{http://www.opengis.net/wms}Dimension").text.split(',')
    
if __name__ == '__main__':

    global verbose 
    verbose = False
    name = False
    count = 1000
    capabilities_doc = None
    layer = None
    # Parse command line arguments.
    argv = sys.argv
    
    
    i = 1
    while i < len(argv):
        arg = argv[i]

        
        if arg == '-count' and i < len(argv)-1:
            count = int(argv[i+1])
            i = i + 1
            
        elif arg == '-capabilities_doc' and i < len(argv)-1:
            capabilities_doc = str(argv[i+1])
            i = i + 1
            
        elif arg == '-layer' and i < len(argv)-1:
            layer = str(argv[i+1])
            i = i + 1
        elif arg == '-verbose':
            verbose = True
        elif arg == '-name':
            name = True
        else:
            print 'Unable to process: %s' % arg
            Usage()

        i = i + 1

    if layer is None:
        print '-layer is required.'
        Usage()

    if capabilities_doc is None:
        print '-capabilities_doc is required.'
        Usage()
        
    # -------------------------------------------------------------------------
    t=[]
    
    if (verbose):
      print "details: "
      print "   layername: " + layer
      print "   capabilities_doc: " + str(capabilities_doc)
      print "Scanning " + capabilities_doc
      
      print ".... Checking " + layer
    tree = ET.parse(capabilities_doc)
    root = tree.getroot()
    layerObj = getLayer(root,layer)
    dims = getDimensions(layerObj)
    
    for time in dims:
        if(name):
            printOut(layer,time)
        else:
            print time




