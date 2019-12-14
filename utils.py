#!/usr/bin/env python3
# -*- coding: utf-8-*-
"""\
Utility routines for CMIP Citaions.

"""

import json
import certifi
import urllib3

__author__ = 'T.Inoue'
__credits__ = 'Copyright (c) 2019 JAMSTEC'
__version__ = 'v20191213'
__date__ = '2019/12/13'

baseGetUrl = 'https://cera-www.dkrz.de/WDCC/ui/cerasearch/cerarest/exportcmip6'
basePostUrl = "http://ceracite.dkrz.de:5000/api/v1/citation"

class Person():
    def __init__(self, givenName=None, familyName=None, email=None, affiliation=None):
        self.givenName = givenName
        self.familyName = familyName
        self.email = email
        self.affiliation = affiliation


    def __str__(self):
        return f'{self.creatorName}, {self.email}, {self.affiliation}'

class Creator(person):
    def __init__(self, *args):
        super().__init__(*args)
        self.creatorName = self.familyName + ', ' + self.givenName

    def __str__(self):
        return f'{self.creatorName}, {self.email}, {self.affiliation}'


def getJSON(source_id=None, activity_id=None,
            institution_id=None, experiment_id=None):
    """
    Access Citation web cite and get JSON for given CV's.
    """

    drs = '.'.join(['CMIP6', activity_id, institution_id, source_id])
    if experiment_id is not None:
        drs += '.' + experiment_id
    fields = {'input': drs}

    print('HTTP access with DRS:', drs)
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    r = http.request_encode_url('GET', baseGetUrl, fields=fields)

    if (r.status != 200):
        print('Bad Status:', r.status)
        d = eval(r.data.decode('utf-8'))
        print(d['error'])
        return None
    jsonData = json.loads(r.data.decode('utf-8'))
    return jsonData



if __name__ == '__main__':
    c = Creator( 'Takahiro', 'Inoue', 'tkhr_i@jamstec.go.jp', 'RESTEC')
    print(c)
    
