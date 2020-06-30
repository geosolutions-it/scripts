#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import time
import logging

sys.path.append('./geowebcache/Python')

from gwcinstance import GWCInstance

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
    Layers: {}
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

# instntiate GWCInstance
gwc = GWCInstance(gwc_rest_url=gwc_rest_url,username=geoserver_username, password=geoserver_password,
                  SSL_cert_verify=True, proxies=proxies)

logger.info("Killing pending tasks")
if layers is not None:
    for layer in layers:
        logger.info("\t killing for layer: {}".format(layer))
        gwc.kill_tasks(layer)
        while (gwc.is_busy(layer)):
            logger.info(".")
            time.sleep(POLL_TIME)
        logger.info("Done.")
else:
    logger.info("Killing all pending tasks")
    gwc.kill_tasks()
    logger.info("Waiting for all pending tasks to finish")
    while (gwc.is_busy()):
        logger.info(".")
        time.sleep(POLL_TIME)
    logger.info("Done.")