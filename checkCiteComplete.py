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


def getInfo():
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


def loadInfo(fname):
    """
    Load local JSON file instead of accessing API
    """

    print(f'Loading from "{fname}"')
    with open(fname, 'r') as f:
        jsonData = json.load(f)
    return jsonData


def saveInfo(docs, fname):
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


def my_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc,
        epilog=epilog)
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False)

    parser.add_argument(
        '--save', type=str, nargs='?', const='', default=None)
    parser.add_argument(
        '--load', type=str, default=None, help='JSON file')

    parser.add_argument(
        '-a', '--mip', '--activity_id', type=str, default=None)
    parser.add_argument(
        '-i', '--inst', '--institution_id', type=str, default=None)
    parser.add_argument(
        '-s', '--model', '--source_id', type=str, default=None)
    parser.add_argument(
        '-e', '--exp', '--experiment_id', type=str, default=None)
    parser.add_argument(
        '-d', '--drsId', type=str, default=None)
    parser.add_argument(
        '-c', '--complete', type=str, default=None,
        help="select complete status (True or False)")

    return parser


def main():

    parser = my_parser()
    a = parser.parse_args()

    if a.verbose:
        print('Arguments:')
        print('  load:', a.load)
        print('  save:', a.save)
        print('  institution_id:', a.inst)
        print('  source_id:', a.model)
        print('  drsId:', a.drsId)
        print('  complete:', a.complete)

    if a.inst:
        params.update({'institutionId': a.inst})
    if a.model:
        params.update({'sourceId': a.model})
    if a.drsId:
        params.update({'drsId': a.drsId})
    if a.complete:
        params.update({'complete': a.complete})

    if a.load:
        docs = loadInfo(a.load)
    else:
        docs = getInfo()

    if not docs:
        return 1

    if a.save is not None:
        saveInfo(docs, a.save)

    checkCompleteness(docs)

    return 0


if __name__ == '__main__':
    exit(main())
