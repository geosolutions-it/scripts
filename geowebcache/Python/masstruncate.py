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
    HTTP Proxy: {}
    HTTPS Proxy: {}
		""".format(
    geoserver_url,
    geoserver_username,
    geoserver_password,
    layers,
    http_proxy,
    https_proxy,
    )
)

gwc_rest_url = '/'.join([geoserver_url.strip('/'), "/gwc/rest".strip('/')])
logger.info("GeoServer GWC REST endpoint: {}".format(gwc_rest_url))

logger.debug("""
	Layers: {}
	DEBUG: {}
		""".format(
    layers,
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

for layer in layers:
    logger.info("\t Seeding layer:".format(layer))
    task = GWCTask(name=layer, type='masstruncate')
    logger.info("\n" + str(task))
    gwc.submit_task(task)

    logger.info("Waiting for all pending tasks to finish")
    while (gwc.is_busy()):
        logger.info(".")
        time.sleep(POLL_TIME)
    logger.info("Done. Exiting")
