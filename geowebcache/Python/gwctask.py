#!/usr/bin/env python

from pprint import pformat

class GWCTask:
    """ GWC Task """
    operation = (
        'seed',
        'reseed',
        'truncate',
        'masstruncate',
    )

    request = None

    def __init__(self, name,  type, bounds=None, srs=None, gridSetId=None, zoomStart=None, zoomStop=None, format=None, parameters=None, threadCount=None):

        if type in ('seed', 'truncate', 'reseed'):
            self.request = {}
            if name is None:
                raise ValueError('GWCTask "name" cannot be None for "{}" operation'.format(type))
            if zoomStart is None:
                raise ValueError('GWCTask "zoomStart" cannot be None for "{}" operation'.format(type))
            if zoomStop is None:
                raise ValueError('GWCTask "zoomStop" cannot be None for "{}" operation'.format(type))
            if format is None:
                raise ValueError('GWCTask "format" cannot be None for "{}" operation'.format(type))
            if threadCount is None:
                raise ValueError('GWCTask "threadCount" cannot be None for "{}" operation'.format(type))
            if srs is None:
                raise ValueError('GWCTask "srs" cannot be None for "{}" operation'.format(type))

            self.request['name'] = name
            self.request['type'] = type
            self.request['zoomStart'] = zoomStart
            self.request['zoomStop'] = zoomStop
            self.request['threadCount'] = threadCount
            self.request['srs'] = {
                'number':srs
            }
            self.request['format'] = format

            if bounds is not None:
                # bounds is expected to be a list
                bounds = {
                    'coords': {
                        'double': bounds
                    }
                }
                self.request['bounds'] = bounds

            if parameters is not None:
                # parameters is a list of key-value pairs
                entry = list()
                for param in parameters:
                    d = {'string': [param[0], param[1]]}
                    entry.append(d)
                self.request['parameters'] = {'entry': entry}
            if gridSetId is not None:
                self.request['gridSetId'] = gridSetId
        elif type in ('masstruncate'):
            self.request = {}
            if name is None:
                raise ValueError('GWCTask "name" cannot be None for "{}" operation'.format(type))
            self.request['name'] = name
            self.request['type'] = type
        else:
            if type is None:
                raise ValueError('GWCTask "type" cannot be None for "{}" operation'.format(type))
            else:
                raise ValueError('GWCTask "type" must be one of: {}'.format(pformat(self.operation)))

    def __str__(self):
        return pformat(self.request, indent=2)