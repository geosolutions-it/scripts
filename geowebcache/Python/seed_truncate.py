#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import time
import logging

sys.path.append('./geowebcache/Python')

from gwcinstance import GWCInstance
from gwctask import GWCTask

# sleep time between 'is_busy' requests to GWC
POLL_TIME = 5

# defaults
NAME = 'tiger:poi'
BOUNDS = None  # example: [6.70, 36.0, 18.5, 47.2]
SRS = '4326'
GRIDSET_ID = 'EPSG:4326'
ZOOM_START_SEED = 0
ZOOM_STOP_SEED = 5
ZOOM_START_TRUNCATE = 0
ZOOM_STOP_TRUNCATE = 7
IMAGE_FORMAT = "image/png"
TYPE = None
THREAD_COUNT = 3

request_defaults_seed = {
    "name": NAME,
    "bounds": BOUNDS,
    "srs": {
        "number": SRS
    },
    "gridSetId": GRIDSET_ID,
    "zoomStart": ZOOM_START_SEED,
    "zoomStop": ZOOM_STOP_SEED,
    "format": IMAGE_FORMAT,
    "type": TYPE,
    "threadCount": THREAD_COUNT
}

request_defaults_truncate = {
    "name": NAME,
    "bounds": BOUNDS,
    "srs": {
        "number": SRS
    },
    "gridSetId": GRIDSET_ID,
    "zoomStart": ZOOM_START_TRUNCATE,
    "zoomStop": ZOOM_STOP_TRUNCATE,
    "format": IMAGE_FORMAT,
    "type": TYPE,
    "threadCount": THREAD_COUNT
}


# fetch Job parameters from environment variables
debug_enabled = os.environ['DEBUG']
geoserver_url = os.environ['GeoServerURL']
geoserver_url = geoserver_url.strip()
geoserver_username = os.environ['GeoServerUsername']
geoserver_password = os.environ['GeoServerPassword']

if 'Layers' in os.environ:
    layers = os.environ['Layers']
    layers = filter(None, layers.splitlines())
    layers = [s.strip() for s in layers]
else:
    layers = list()

if 'SequenceNumbers' in os.environ:
    sequence_numbers = os.environ['SequenceNumbers']
    sequence_numbers = filter(None, sequence_numbers.splitlines())
    sequence_numbers = [s.strip() for s in sequence_numbers]
else:
    sequence_numbers = list()

if 'Bounds' in os.environ:
    bounds = os.environ['Bounds']
    bounds = filter(None, bounds.splitlines())
    bounds = [s.strip() for s in bounds]
else:
    bounds = None()


if 'HTTP_PROXY' in os.environ:
    http_proxy = os.environ['HTTP_PROXY']
else:
    http_proxy = None

if 'HTTPS_PROXY' in os.environ:
    https_proxy = os.environ['HTTPS_PROXY']
else:
    https_proxy = None

if http_proxy or https_proxy:
    proxies = {
        "http"  : http_proxy,
        "https" : https_proxy
    }
else:
    proxies = None

# initialize logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logl = logging.DEBUG if debug_enabled.lower() == 'true' else logging.INFO
logger.setLevel(logl)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info("""
    GeoServerURL: {}
    GeoServerUsername: {}
    GeoServerPassword: {}
    Bounds: {}
    HTTP Proxy: {}
    HTTPS Proxy: {}
		""".format(
    geoserver_url,
    geoserver_username,
    geoserver_password,
    bounds,
    http_proxy,
    https_proxy,
    )
)

gwc_rest_url = '/'.join([geoserver_url.strip('/'), "/gwc/rest".strip('/')])
logger.info("GeoServer GWC REST endpoint: {}".format(gwc_rest_url))

logger.debug("""
	Layers: {}
	SequenceNumbers: {}
	Bounds: {}
	DEBUG: {}
		""".format(
    layers,
    sequence_numbers,
    bounds,
    debug_enabled,
    )
)

# instntiate GWCInstance
gwc = GWCInstance(gwc_rest_url=gwc_rest_url,username=geoserver_username, password=geoserver_password,
                  SSL_cert_verify=True, proxies=proxies)

#layer = 'tiger:marble'
#bounds = [7, 35, 18, 45]
logger.info("\t seeding layer: {} with Bounds: {}".format(layers, bounds))
task = GWCTask(name=layers, type='seed',
               bounds=bounds,
               srs=request_defaults_seed['srs']['number'],
               gridSetId=request_defaults_seed['gridSetId'],
               zoomStart=request_defaults_seed['zoomStart'],
               zoomStop=request_defaults_seed['zoomStop'],
               format=request_defaults_seed['format'],
#               parameters=[
#                   ('CQL_FILTER', "seq='{}'".format(seq))
#               ],
               threadCount=request_defaults_seed['threadCount']
               )
logger.debug(task)
gwc.submit_task(task)
while (gwc.is_busy()):
    logger.debug("GWC is busy, waiting {} seconds".format(POLL_TIME))
    time.sleep(POLL_TIME)