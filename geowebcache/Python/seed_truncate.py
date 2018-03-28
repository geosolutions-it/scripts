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
NAME = 'earthmodel:Natural_Earth'
BOUNDS = None  # example: {"coords":{"double":["-14.0","22.0","66.0","72.0"]}}
SRS = '4326'
GRIDSET_ID = 'EPSG:4326_512'
ZOOM_START = 1
ZOOM_STOP = 4
IMAGE_FORMAT = "image/png"
TYPE = None
THREAD_COUNT = 3

request_defaults = {
    "name": NAME,
    "bounds": BOUNDS,
    "srs": {
        "number": SRS
    },
    "gridSetId": GRIDSET_ID,
    "zoomStart": ZOOM_START,
    "zoomStop": ZOOM_STOP,
    "format": IMAGE_FORMAT,
    "type": TYPE,
    "threadCount": THREAD_COUNT
}

# fetch Job parameters from environment variables
debug_enabled = os.environ['DEBUG']
geoserver_url = os.environ['GeoServerURL']
geoserver_username = os.environ['GeoServerUsername']
geoserver_password = os.environ['GeoServerPassword']

layers_sequenced = os.environ['LayersSequenced']
layers_sequenced = filter(None, layers_sequenced.splitlines())

sequence_numbers = os.environ['SequenceNumbers']
sequence_numbers = filter(None, sequence_numbers.splitlines())

layers_unsequenced = os.environ['LayersUnsequenced']
layers_unsequenced = filter(None, layers_unsequenced.splitlines())

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
		""".format(
    geoserver_url,
    geoserver_username,
    geoserver_password,
    )
)

gwc_rest_url = '/'.join([geoserver_url.strip('/'), "/gwc/rest".strip('/')])
logger.info("GeoServer GWC REST endpoint: {}".format(gwc_rest_url))

logger.debug("""
	LayersSequenced: {}
	SequenceNumbers: {}
	LayersUnsequenced: {}
	DEBUG: {}
		""".format(
    layers_sequenced,
    sequence_numbers,
    layers_unsequenced,
    debug_enabled,
    )
)

# instntiate GWCInstance
gwc = GWCInstance(gwc_rest_url=gwc_rest_url,username=geoserver_username, password=geoserver_password, SSL_cert_verify=True)

# masstruncate UnSequenced Layers
logger.info("Masstruncate UnSequenced Layers")
for layer in layers_unsequenced:
    logger.info("\t tuncating layer: {}".format(layer))
    task = GWCTask(name=layer, type='masstruncate')
    logger.debug(task)
    gwc.submit_task(task)
    while(gwc.is_busy()):
        logger.debug("GWC is busy, waiting {} seconds".format(POLL_TIME))
        time.sleep(POLL_TIME)


# seed UnSequenced Layers
logger.info("Seeding UnSequenced Layers")
for layer in layers_unsequenced:
    logger.info("\t seeding layer: {}".format(layer))
    task = GWCTask(name=layer, type='seed',
                   bounds=request_defaults['bounds'],
                   srs=request_defaults['srs']['number'],
                   gridSetId=request_defaults['gridSetId'],
                   zoomStart=request_defaults['zoomStart'],
                   zoomStop=request_defaults['zoomStop'],
                   format=request_defaults['format'],
                   parameters=None,
                   threadCount=request_defaults['threadCount']
                   )
    logger.debug(task)
    gwc.submit_task(task)
    while(gwc.is_busy()):
        logger.debug("GWC is busy, waiting {} seconds".format(POLL_TIME))
        time.sleep(POLL_TIME)


# truncate Sequenced Layers
logger.info("Truncating Sequenced Layers")
for layer in layers_unsequenced:
    for seq in sequence_numbers:
        logger.info("\t tuncating layer:  with Sequence: {}".format(layer, seq))
        task = GWCTask(name=layer, type='truncate',
                       bounds=request_defaults['bounds'],
                       srs=request_defaults['srs']['number'],
                       gridSetId=request_defaults['gridSetId'],
                       zoomStart=request_defaults['zoomStart'],
                       zoomStop=request_defaults['zoomStop'],
                       format=request_defaults['format'],
                       parameters=[
                           ('CQL_FILTER', "seq='{}'".format(seq))
                       ],
                       threadCount=request_defaults['threadCount']
                       )
        logger.debug(task)
        gwc.submit_task(task)
        while(gwc.is_busy()):
            logger.debug("GWC is busy, waiting {} seconds".format(POLL_TIME))
            time.sleep(POLL_TIME)


# seed UnSequenced Layers
logger.info("Seeding Sequenced Layers")

# ignoring bounds
for layer in layers_sequenced:
    for seq in sequence_numbers:
        logger.info("\t seeding layer: {} with Sequence: {}".format(layer, seq))
        param = ('cql_filter', "seq='{}'".format(seq))
        task = GWCTask(name=layer, type='seed',
                       bounds=request_defaults['bounds'],
                       srs=request_defaults['srs']['number'],
                       gridSetId=request_defaults['gridSetId'],
                       zoomStart=request_defaults['zoomStart'],
                       zoomStop=request_defaults['zoomStop'],
                       format=request_defaults['format'],
                       parameters=[
                           ('CQL_FILTER', "seq='{}'".format(seq))
                       ],
                       threadCount=request_defaults['threadCount']
                       )
        logger.debug(task)
        gwc.submit_task(task)
        while(gwc.is_busy()):
            logger.debug("GWC is busy, waiting {} seconds".format(POLL_TIME))
            time.sleep(POLL_TIME)