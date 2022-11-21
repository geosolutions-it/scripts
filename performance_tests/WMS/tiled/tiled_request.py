#!/usr/bin/env python

import random
import math
import string
import sys
import os
from os import listdir
from os.path import isfile, join
from xml.dom import minidom
# =============================================================================


def Usage():
    print('Usage: tiled_request.py [-count n] [-region minx miny maxx maxy]')
    print('                  [-auxiliary_csv <path_to_csv>] [-gridset_dir <path_to_gridset_xml_definitions>]')
    print('                  [-gridset gridsetName] [-levels l1,l2,l3] [-srs] [-verbose]')
    print(' Generate outputs with: WIDTH;HEIGHT;BBOX(MINX,MINY,MAXX,MAXY)[;ESPG:CODE]')
    print(' \"EPSG:CODE\" being produced only in case the -srs option has been specified')
    sys.exit(1)

# =============================================================================


def getGridset(gridset_dir):
    if (verbose):
        print(f"Scanning {gridset_dir}")
    onlyfiles = []
    onlyfiles = listdir(gridset_dir)
    for file in onlyfiles:
        if (verbose):
            print(f".... Checking {file}")
        tree = minidom.parse(join(gridset_dir, file))
        itemlist = tree.getElementsByTagName("gridSet")
        for item in itemlist:
            for child in item.getElementsByTagName("name"):
                element = child.childNodes[0]
                name = element.nodeValue
                if (name == gridsetName):
                    if (verbose):
                        print(f"......... Specified gridset {name} found on {file}")
                    return item


def getTileSize(gridset):
    tilesize = []
    if gridset:
        itemlist = gridset.getElementsByTagName("tileWidth")
        for item in itemlist:
            element = item.childNodes[0]
            tilesize.append(int(element.nodeValue))
            break
        itemlist = gridset.getElementsByTagName("tileHeight")
        for item in itemlist:
            element = item.childNodes[0]
            tilesize.append(int(element.nodeValue))
            break
    else:
        tilesize = [256, 256]
    return tilesize


def getTilesOrigin(gridset):
    tilesOrigin = []
    if gridset:
        itemlist = gridset.getElementsByTagName("coords")
        for item in itemlist:
            for coord in item.getElementsByTagName("double"):
                tilesOrigin.append(float(coord.childNodes[0].nodeValue))
    else:
        tilesOrigin = list(region)
    return tilesOrigin


def getResolutions(gridset):
    resolutions = []
    if gridset:
        itemlist = gridset.getElementsByTagName("resolutions")
        for item in itemlist:
            for res in item.getElementsByTagName("double"):
                resolutions.append(float(res.childNodes[0].nodeValue))
    else:
        resolutions = []
    return resolutions


def getSRS(gridset):
    if gridset:
        itemlist = gridset.getElementsByTagName("srs")
        for item in itemlist:
            for num in item.getElementsByTagName("number"):
                return f"EPSG:{str(num.childNodes[0].nodeValue)}"
    return ""


def printOutLine(line, width, height, bbox, srsName):
    print(f"{line + str(width)};{str(height)};{str(bbox[0])},{str(bbox[1])},{str(bbox[2])},{str(bbox[3])}{f';{srsName}' if srs else ''}")


if __name__ == '__main__':

    global verbose
    global region
    global srs
    layer = None
    srs = False
    verbose = False
    tiles_origin = None
    region = None
    minres = None
    maxres = None
    count = 1000
    entries = None
    gridsetName = None
    auxiliary_csv = None
    gridset_dir = None
    levels = '1'
    res = None

    # Parse command line arguments.
    argv = sys.argv

    i = 1
    while i < len(argv):
        arg = argv[i]

        if arg == '-region' and i < len(argv) - 4:
            region = (float(argv[i + 1]), float(argv[i + 2]),
                      float(argv[i + 3]), float(argv[i + 4]))
            i = i + 4
        elif arg == '-layer' and i < len(argv) - 1:
            layer = str(argv[i + 1])
            i = i + 1
        elif arg == '-count' and i < len(argv) - 1:
            count = int(argv[i + 1])
            i = i + 1
        elif arg == '-auxiliary_csv' and i < len(argv) - 1:
            auxiliary_csv = str(argv[i + 1])
            i = i + 1
        elif arg == '-gridset_dir' and i < len(argv) - 1:
            gridset_dir = str(argv[i + 1])
            i = i + 1
        elif arg == '-gridset' and i < len(argv) - 1:
            gridsetName = str(argv[i + 1])
            i = i + 1
        elif arg == '-levels' and i < len(argv) - 1:
            levels = str(argv[i + 1])
            i = i + 1
        elif arg == '-verbose':
            verbose = True
        elif arg == '-srs':
            srs = True
        else:
            print(f'Unable to process: {arg}')
            Usage()

        i = i + 1

    if region is None:
        print('-region is required.')
        Usage()

    if gridsetName is None:
        print('-gridset is required.')
        Usage()

    if levels is None:
        print('-levels is required.')
        Usage()

    if gridset_dir is None:
        print('-gridset_dir is required.')
        Usage()

    # -------------------------------------------------------------------------
    t = []
    if not (auxiliary_csv is None):
        entries = open(auxiliary_csv)
        for line in entries.readlines():
            t.append(line.strip())
        entries.close()

    # List gridsets definitions and loop over them looking for the definition

    gridset = getGridset(gridset_dir)
    tileSize = getTileSize(gridset)
    tiles_origin = getTilesOrigin(gridset)
    resolutions = getResolutions(gridset)
    srsName = getSRS(gridset) or gridsetName
    if (verbose):
        print("gridset details: ")
        print(f"   name: {gridsetName}")
        print(f"   srs:  {srsName}")
        print(f"   tileSize: {str(tileSize)}")
        print(f"   bbox: {str(tiles_origin)}")
        print(f"   resolutions: {str(resolutions)}")
        print(f"   resolutions: {str(resolutions)}")
    levelIndexes = levels.split(',')
    numResolutions = len(resolutions)
    for levelIndex in levelIndexes:
        if (int(levelIndex) > (numResolutions - 1)):
            print(f"levelIndex must be in range 0 - {str(numResolutions - 1)}")
            sys.exit(1)
    width = tileSize[0]
    height = tileSize[1]
    numLevels = len(levelIndexes)
    hasAuxFile = len(t) > 0
    while count > 0:
        levelIndex = random.randint(0, numLevels - 1)
        res = resolutions[int(levelIndexes[levelIndex])]

        tile_min_x = int(math.floor((random.uniform(region[0], region[1]) - tiles_origin[0]) / (width * res)))
        tile_min_y = int(math.floor((random.uniform(region[2], region[3])- tiles_origin[1]) / (height * res)))

        bbox_x0 = tiles_origin[0] + tile_min_x * width * res
        bbox_y0 = tiles_origin[1] + tile_min_y * height * res

        bbox = (bbox_x0,
                bbox_y0,
                bbox_x0 + 1 * width * res,
                bbox_y0 + 1 * height * res)

        count = count - 1
        if (hasAuxFile):
            for line in t:
                printOutLine(f"{line};", width, height, bbox, srsName)
        else:
            printOutLine(f"{layer};", width, height, bbox, srsName)
