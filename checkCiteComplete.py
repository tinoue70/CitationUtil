#!/usr/bin/env python3
# -*- coding: utf-8-*-
"""\
Check the completion of the data reference information via the
specific API provided by the citation service.

---
Access API URL with several attributes, the data reference information
in JSON format is returned.  Valid attributes are: `institutionId`,
`sourceId`, `complete` (true|false), `drsId`.

See <https://redmine.dkrz.de/projects/cmip6-lta-and-data-citation/wiki/Wiki#Information-for-ESGF-Data-Node-Managers-and-other-external-service-providers>.
"""
import urllib3
import certifi
import json
import argparse
import datetime

__author__ = 'T.Inoue'
__credits__ = 'Copyright (c) 2019 RIST'
__version__ = 'v20190626'
__date__ = '2019/06/26'

base_url = ("https://cera-www.dkrz.de/WDCC/ui/cerasearch/"
            "cerarest/cmip6Citations")
params = {
    # 'institutionId': 'MIROC',
    # 'sourceId': 'MIROC6',
    # 'complete': 'false',
    # 'drsId':'CMIP6.CMIP.MIROC.MIROC6',
}

desc, epilog = __doc__.split('---')


def my_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc,
        epilog=epilog)
    parser.add_argument(
        '-s', '--save', type=str, nargs='?', const='', default=None)
    parser.add_argument(
        '-l', '--load', type=str, default=None, help='JSON file')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False)

    parser.add_argument(
        '-I', '--institutionId', type=str, default=None)
    parser.add_argument(
        '-S', '--sourceId', type=str, default=None)
    parser.add_argument(
        '-D', '--drsId', type=str, default=None)
    parser.add_argument(
        '-c', '--complete', type=str, default=None,
        help="select complete status (True or False)")

    return parser


def getJSON():
    """
    Access API and get information as JSON format.
    """
    print('HTTP access with params:', params)
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    r = http.request_encode_url('GET', base_url, fields=params)

    if (r.status != 200):
        print('Bad Status:', r.status)
        d = eval(r.data.decode('utf-8'))
        print(d['error'])
        return None
    jsonData = json.loads(r.data.decode('utf-8'))
    return jsonData


def loadJSON(fname):
    """
    Load local JSON file instead of accessing API
    """

    print(f'Loading from "{fname}"')
    with open(fname, 'r') as f:
        jsonData = json.load(f)
    return jsonData


def saveJSON(docs, fname):
    if not fname:
        datestr = datetime.date.today().strftime('%Y%m%d')

        fname = datestr+'Citation'
        if 'institutionId' in params:
            fname += '.' + params['institutionId']
        if 'sourceId' in params:
            fname += '.' + params['sourceId']
        fname += '.json'
    with open(fname, 'w') as f:
        json.dump(docs, f, indent=2)
    print(f'Saved to "{fname}"')


def checkCompleteness(docs):
    print('Check citation completeness:')
    for d in docs:
        print(f'  {d["DRS_ID"]}: {d["CITATION_COMPLETED"]}')


def main():

    parser = my_parser()
    a = parser.parse_args()

    if a.debug:
        print('dbg: arguments:')
        print('  load:', a.load)
        print('  save:', a.save)
        print('  institutionId:', a.institutionId)
        print('  sourceId:', a.sourceId)
        print('  drsId:', a.drsId)
        print('  complete:', a.complete)

    if a.institutionId:
        params.update({'institutionId': a.institutionId})
    if a.sourceId:
        params.update({'sourceId': a.sourceId})
    if a.drsId:
        params.update({'drsId': a.drsId})
    if a.complete:
        params.update({'complete': a.complete})

    if a.load:
        docs = loadJSON(a.load)
    else:
        docs = getJSON()

    if not docs:
        return 1

    if a.save is not None:
        saveJSON(docs, a.save)

    checkCompleteness(docs)

    return 0


if __name__ == '__main__':
    exit(main())
