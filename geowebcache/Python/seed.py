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

if 'Style' in os.environ:
    style = os.environ['Style']
else:
    style = None

if 'ImageFormat' in os.environ:
    image_format = os.environ['ImageFormat']
else:
    image_format = None

if 'SequenceNumbers' in os.environ:
    sequence_numbers = os.environ['SequenceNumbers']
    sequence_numbers = filter(None, sequence_numbers.splitlines())
    sequence_numbers = [s.strip() for s in sequence_numbers]
else:
    sequence_numbers = list()

if 'Bounds' in os.environ:
    bounds = os.environ['Bounds']
    bounds = bounds.split(',')
    bounds = [s.strip() for s in bounds]
else:
    bounds = None

if 'StateID' in os.environ:
    state_id = os.environ['StateID']
else:
    state_id = None

if 'ZoomStart' in os.environ:
    zoom_start = os.environ['ZoomStart']
else:
    zoom_start = None

if 'ZoomStop' in os.environ:
    zoom_stop = os.environ['ZoomStop']
else:
    zoom_stop = None

if 'ThreadCount' in os.environ:
    thread_count = os.environ['ThreadCount']
else:
    thread_count = None

if 'SRS' in os.environ:
    srs = os.environ['SRS']
else:
    srs = None

if 'GridSetID' in os.environ:
    gridset_id = os.environ['GridSetID']
else:
    gridset_id = None

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
    Layer: {}
    Style: {}
    ImageFormat: {}
    Bounds: {}
    StateID: {}
    SRS: {}
    GridSetID: {}
    ThreadCount: {}
    HTTP Proxy: {}
    HTTPS Proxy: {}
		""".format(
    geoserver_url,
    geoserver_username,
    geoserver_password,
    layers,
    style,
    image_format,
    bounds,
    state_id,
    srs,
    gridset_id,
    thread_count,
    http_proxy,
    https_proxy,
    )
)

gwc_rest_url = '/'.join([geoserver_url.strip('/'), "/gwc/rest".strip('/')])
logger.info("GeoServer GWC REST endpoint: {}".format(gwc_rest_url))

logger.debug("""
	Layers: {}
	Style: {}
	ImageFormat: {}
	SequenceNumbers: {}
	Bounds: {}
	StateID: {}
	SRS: {}
	GridSetID: {}
	ThreadCount: {}
	DEBUG: {}
		""".format(
    layers,
    style,
    image_format,
    sequence_numbers,
    bounds,
    state_id,
    srs,
    gridset_id,
    thread_count,
    debug_enabled,
    )
)

# instntiate GWCInstance
gwc = GWCInstance(gwc_rest_url=gwc_rest_url,username=geoserver_username, password=geoserver_password,
                  SSL_cert_verify=True, proxies=proxies)


if gwc.is_busy():
    logger.info("There are already pending tasks in GWC. Waiting for pending tasks to finish before moving on")
    while (gwc.is_busy()):
        logger.info(".")
        time.sleep(POLL_TIME)
    logger.info("No more pending tasks. Moving on")

# Preparing Parameter filters
parameters = list()
if state_id:
    parameters.append(('VIEWPARAMS', 'STATE_ID:'+str(state_id)))
if style:
    parameters.append(('STYLES', style))

for layer in layers:
    logger.info("\t Seeding layer:".format(layer))
    task = GWCTask(name=layer, type='seed',
                   bounds=bounds,
                   srs=srs,
                   gridSetId=gridset_id,
                   zoomStart=zoom_start,
                   zoomStop=zoom_stop,
                   format=image_format,
                   parameters=parameters,
                   threadCount=thread_count
                   )
    logger.info("\n" + str(task))
    gwc.submit_task(task)

    logger.info("Waiting for all pending tasks to finish")
    while (gwc.is_busy()):
        logger.info(".")
        time.sleep(POLL_TIME)
    logger.info("Done. Exiting")
