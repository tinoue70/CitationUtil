#!/usr/bin/env python3
# -*- coding: utf-8-*-
"""\
Submit CMIP6 Citation info of experiment granularity.

---
This script gets base (MIP-granularity) info from the citation service
or local JSON file, adds experiment informations, then puts it  back to
the citaion service.

You have to specify MIP(`activity_id`), model(`source_id`) to get base
info, and have to specify experiments(`experiment_id`) to submit
experiment-granularity info.
"""
from utils import getJSON
import json
import certifi
import urllib3
import argparse

__author__ = 'T.Inoue'
__credits__ = 'Copyright (c) 2019 RIST'
__version__ = 'v20190626'
__date__ = '2019/06/26'

# baseGetUrl = 'https://cera-www.dkrz.de/WDCC/ui/cerasearch/cerarest/exportcmip6'
# basePostUrl = "http://ceracite.dkrz.de:5000/api/v1/citation"

mip = 'CMIP'
model = 'MIROC6'
inst = 'MIROC'
experiments = ('historical')

# model = 'NICAM16-7S'
# mip = 'HighResMIP'
# experiments = (
#     'highresSST-present',
# )

desc, epilog = __doc__.split('---')


def my_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc, epilog=epilog, )
    parser.add_argument('-v', '--verbose',
                        dest='verbose', action='store_true',
                        help='be verbose.',
                        )
    parser.add_argument('-c', '--checkonly',
                        dest='checkonly', action='store_true',
                        help='Perform check only.')
    parser.add_argument('-g', '--getonly',
                        dest='getonly', action='store_true',
                        help='Get base JSON, only.')
    parser.add_argument('experiments',
                        metavar='exp', type=str, nargs='*',
                        help='experiments to submit')
    parser.add_argument('-s', '--model', '--source_id',
                        type=str,
                        help='model(source_id)',
                        default=model)
    parser.add_argument('-a', '--mip', '--activity_id',
                        type=str,
                        help='MIP(activity_id)',
                        default=mip)
    parser.add_argument('-i', '--inst', '--institution_id',
                        type=str,
                        help='institution(institution_id)',
                        default=inst)

    parser.add_argument('-l', '--loadfile',
                        type=str,
                        help='Load base JSON from local file', nargs='?',
                        default=None, const='')
    return parser


# def getJSON(source_id='MIROC6', activity_id='CMIP',
#             institution_id='MIROC', experiment_id=None):
#     """
#     Access Citation web cite and get JSON for given CV's.
#     """

#     drs = '.'.join(['CMIP6', activity_id, institution_id, source_id])
#     if experiment_id is not None:
#         drs += '.' + experiment_id
#     fields = {'input': drs}

#     print('HTTP access with DRS:', drs)
#     http = urllib3.PoolManager(
#         cert_reqs='CERT_REQUIRED',
#         ca_certs=certifi.where())
#     r = http.request_encode_url('GET', baseGetUrl, fields=fields)

#     if (r.status != 200):
#         print('Bad Status:', r.status)
#         d = eval(r.data.decode('utf-8'))
#         print(d['error'])
#         return None
#     jsonData = json.loads(r.data.decode('utf-8'))
#     return jsonData


def loadJSON(fname=None,
             source_id=None, activity_id=None,
             institution_id='MIROC', experiment_id=None):
    """
    Load local JSON file instead of accessing Citation web cite.
    """

    if fname is None or fname is '':
        if not all([source_id, activity_id, institution_id]):
            return None
        else:
            fname = '.'.join(['CMIP6', activity_id, institution_id, source_id])
        if (experiment_id is not None):
            fname += '.' + experiment_id
        fname += '.json'
    print(f'Loading from "{fname}"')

    with open(fname) as f:
        jsonData = json.load(f)
    return jsonData


def addExperiment(inData, experiment):
    """
    Convert from MIP granularity data to experiment granularity data;
    - add `experiment` to title,
    - add `experiment` to subject as DRS,
    - remove identifier.

    Returns deepcopy()_ed data, given `inData` is preserved.
    """

    from copy import deepcopy
    data = deepcopy(inData)

    data['subjects'][0]['subject'] += '.' + experiment
    data['titles'][0] += ' ' + experiment

    # delete identifier
    if 'identifier' in data:
        del data['identifier']

    return data


def putBack(data, extra='check'):
    """
    Put back modified JSON to the citaion web.

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
    encoded_body = json.dumps(data).encode('utf-8')

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


def main():

    parser = my_parser()
    a = parser.parse_args()

    if (a.verbose):
        print('Configuration:')
        print('  checkonly:', a.checkonly)
        print('  getonly:', a.getonly)
        print('  model:', a.model)
        print('  mip:', a.mip)
        print('  experiments:', a.experiments)
        if (a.loadfile is None):
            print('  loadfile: not specified')
        elif (a.loadfile):
            print('  loadfile: specified explicitly:', a.loadfile)
        else:
            print('  loadfile: specified but no a.')

    if (a.loadfile is None):
        base = getJSON(source_id=a.model, activity_id=a.mip, institution_id=a.inst)
    else:
        base = loadJSON(a.loadfile, source_id=a.model, activity_id=a.mip)

    if (base is None):
        exit(1)

    base_title = base['titles'][0]
    base_subject = base['subjects'][0]['subject']

    if (a.verbose):
        print('base title:', base_title)
        print('base subject:', base_subject)

    if (a.getonly):
        fname = base_subject + '.json'
        with open(fname, 'w') as f:
            print('Saving base data to:', fname)
            json.dump(base, f, indent=2)
    else:
        for exp in a.experiments:
            data = addExperiment(base, exp)     # base is preserved.
            data_subject = data['subjects'][0]['subject']
            print('Checking', data_subject)
            status = putBack(data, extra='check')
            if (not isinstance(status, Exception)):
                if (a.verbose):
                    print("Check status:", status)
                if (status == 200) and (not a.checkonly):
                    print('Submitting', data_subject)
                    status = putBack(data, extra=None)
                    if (status != 200):
                        print(status)
    print('Done.')

    return 0


if __name__ == '__main__':
    exit(main())
