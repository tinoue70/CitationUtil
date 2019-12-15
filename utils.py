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
    def __init__(self, givenName=None, familyName=None,
                 email=None, affiliation=None):
        self.givenName = givenName
        self.familyName = familyName
        self.email = email
        self.affiliation = affiliation

    def __str__(self):
        return f'{self.creatorName}, {self.email}, {self.affiliation}'


class Creator(Person):
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


def loadJSON(fname=None):
    """
    Load local JSON file instead of accessing Citation web cite.
    """

    with open(fname) as f:
        jsonData = json.load(f)
    return jsonData


def setJSONfname(source_id=None, activity_id=None,
                 institution_id=None, experiment_id=None):
    """
    Construct JSON filename.
    """

    if not all([source_id, activity_id, institution_id]):
        return None
    else:
        fname = '.'.join(['CMIP6', activity_id, institution_id, source_id])
    if (experiment_id is not None):
        fname += '.' + experiment_id
    fname += '.json'

    return fname


def postJSON(jsonData, extra='check'):
    """
    Post JSON to the citaion web.

    Based on "citation_client.py".

    `extra` must be ``test``, ``check``, ``tcheck`` or ``None``.

    Returns response status of request.

    Note that if `extra` is ``check``, response status is other than 200
    if something is wrong.
    """
    import netrc

    url = basePostUrl
    extra_list = ('test', 'check', 'tcheck')
    if (extra is not None) and (extra in extra_list):
        extra_param = '?' + extra + '=1'
        url += extra_param

    info = netrc.netrc()
    login, account, password = info.authenticators("cera")
    headers = urllib3.util.make_headers(basic_auth=login+':'+password)
    headers['Content-Type'] = "application/json"

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    encoded_body = json.dumps(jsonData).encode('utf-8')

    try:
        r = http.request_encode_body('POST', url,
                                     headers=headers, body=encoded_body)
    except Exception as e:
        print('Error:', e)
        return e

    if (r.status != 200):
        print('Bad Status:', r.status)
        d = eval(r.data.decode('utf-8'))
        print(d['error'])
    else:
        print(r.data.decode('utf-8'))

    return r.status


if __name__ == '__main__':
    c = Creator('Takahiro', 'Inoue', 'tkhr_i@jamstec.go.jp', 'RESTEC')
    print(c)
