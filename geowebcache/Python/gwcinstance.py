#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

import json
import requests

GWC_TASK_STATUS = ['ABORTED', 'PENDING', 'RUNNING', 'DONE']

class GWCInstance:
    """ GWCInstance """
    def __init__(self, gwc_rest_url, username, password):
        if gwc_rest_url is None:
            raise ValueError('GWCInstance "gwc_rest_url" cannot be None')
        if username is None:
            raise ValueError('GWCInstance "username" cannot be None')
        if password is None:
            raise ValueError('GWCInstance "password" cannot be None')

        self.gwc_rest_url = gwc_rest_url
        self.username = username
        self.password = password

    def is_busy(self):
        """ Return True if there is any task running """
        tasks_array = self.get_tasks()
        return True if len(tasks_array) > 0 else False

    def submit_task(self, gwctask):
        """" Submit new task """
        url  = self.gwc_rest_url.strip('/')
        if gwctask.request['type'] in ('seed', 'truncate', 'reseed'):
            layer = gwctask.request['name']
            url = '/'.join(
                [url , "/seed/{}.json".format(layer).strip('/')]
            )
            payload = json.dumps({'seedRequest':gwctask.request}, indent=4)
        elif gwctask.request['type'] == 'masstruncate':
            layer = gwctask.request['name']
            url = '/'.join(
                [url, "/masstruncate".strip('/')]
            )
            payload = "<truncateLayer><layerName>{}</layerName></truncateLayer>".format(layer)
        try:
            r = requests.post(url, auth=(self.username, self.password), data=payload)
            r.raise_for_status()
        except requests.Timeout as e:
            print("Cannot connect to GWC instance. Request Timeout")
            print(e)
            return False
        except requests.ConnectionError as e:
            print("Cannot connect to GWC instance. Connection Error")
            print(e)
            return False
        except requests.TooManyRedirects as e:
            print("Cannot connect to GWC instance. Too many redirects")
            print(e)
            return None
        except requests.HTTPError as e:
            print("HTTP request failed with code {}".format(r.status_code))
            print(e)
            return False
        except requests.RequestException as e:
            print("HTTP request failed")
            print(e)
            return False
        return True

    def kill_tasks(self, layer=None, filter='all'):
        """ Kill running tasks"""
        url  = self.gwc_rest_url.strip('/')
        if layer is not None:
            url = '/'.join(
                [url, "/seed/{}".format(layer).strip('/')]
            )
        else:
            url = '/'.join( [url, "/seed".strip('/')] )
        payload = 'kill_all={}'.format(filter)
        try:
            r = requests.post(url, auth=(self.username, self.password), data=payload)
        except requests.ConnectionError:
            print("Cannot connect to GWC instance")
            return None
        if r.status_code != requests.codes.ok:
            print("HTTP request failed with code {}".format(r.status_code))
            return None

    def get_tasks(self, layer=None):
        """ Return task status of all tasks """
        if layer is None:
            url = '/'.join(
                [self.gwc_rest_url, "/seed.json".strip('/')]
            )
        else:
            url = '/'.join(
                [self.gwc_rest_url, "/seed/{}.json".format(layer).strip('/')]
            )
        try:
            r = requests.get(url, auth=(self.username, self.password))
        except requests.ConnectionError:
            print("Cannot connect to GWC instance")
            return None
        if r.status_code != requests.codes.ok:
            print("HTTP request failed with code {}".format(r.status_code))
            return None
        tasks_array = r.json()['long-array-array']
        return tasks_array