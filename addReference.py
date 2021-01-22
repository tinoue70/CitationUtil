#!/usr/bin/env python3
# -*- coding: utf-8-*-

"""\
Add reference to CMIP6 Citation info JSON file.

---
This script reads in JSON file, add given reference info, write back to the same file.

Use getJSON.py to get original JSON file.

Use postJSON.py to check/post created JSON file.

"""

import json
import argparse
from utils import loadJSON, getJSON, postJSON, setJSONfname
__author__ = 'T.Inoue'
__credits__ = 'Copyright (c) 2019 RIST'
__version__ = 'v20190626'
__date__ = '2019/06/26'

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
    parser.add_argument('-i', '--inst', '--institution_id',
                        type=str,
                        help='institution(institution_id)',
                        default=inst)
    parser.add_argument('-s', '--model', '--source_id',
                        type=str,
                        help='model(source_id)',
                        default=model)
    parser.add_argument('-a', '--mip', '--activity_id',
                        type=str,
                        help='MIP(activity_id)',
                        default=mip)
    parser.add_argument('-e', '--experiment',
                        metavar='exp', type=str,
                        help='experiment to submit',
                        default=None)
    parser.add_argument('-l', '--loadfile',
                        type=str,
                        help='Load base JSON from local file', nargs='?',
                        default=None, const='')
    parser.add_argument('reference',
                        type=str,
                        help='reference(DOI)')

    return parser


def addReference(inData, reference):
    """
    """

    from copy import deepcopy
    data = deepcopy(inData)

    existing_refs = [x for x in data['relatedIdentifiers'] if x['relationType']=='References']
    ref_list = [ x['relatedIdentifier'] for x in existing_refs]

    if ( reference not in ref_list):
        print(reference, 'is NOT in existing references, adding it.')
    else:
        print(reference, 'is in existing references, do Noting.')
        return None # temporary.

    r = {"relatedIdentifier": reference,
         "relatedIdentifierType": 'DOI',
         "relationType": 'References'}

    data['relatedIdentifiers'].append(r)
    return data


def main():

    parser = my_parser()
    a = parser.parse_args()

    if (a.verbose):
        print('Configuration:')
        # print('  dopost:', a.dopost)
        print('  reference:', a.reference)
        print('  model:', a.model)
        print('  mip:', a.mip)
        print('  experiment:', a.experiment)
        if (a.loadfile is None):
            print('  loadfile: not specified')
        elif (a.loadfile==''):
            print('  loadfile: name not given')
        else:
            pritn('  loadfile:', a.loadfile)

    
    if (a.loadfile == ''):
        a.loadfile = setJSONfname(source_id=a.model, activity_id=a.mip,
                                  institution_id=a.inst, experiment_id=a.experiment)
        # if (a.verbose):
        #     print('loadfile: set as:', a.loadfile)

    if (a.loadfile is None):
        base = getJSON(source_id=a.model, activity_id=a.mip,
                       institution_id=a.inst, experiment_id=a.experiment)
    else:
        # if (a.verbose):
        #     print('file:', a.loadfile)
        print('load from file:', a.loadfile)
        base = loadJSON(a.loadfile)

    if (base is None):
        exit(1)

    # base_title = base['titles'][0]
    # base_subject = base['subjects'][0]['subject']

    # if (a.verbose):
    #     print('base title:', base_title)
    #     print('base subject:', base_subject)

    data = addReference(base, a.reference) # base is preserved
    if data is not None:
        fname = setJSONfname(a.model, a.mip, a.inst, a.experiment)
        with open(fname, 'w') as f:
            print('Saving base data to:', fname)
            json.dump(data, f, indent=2)

    print('Done.')

    return 0


if __name__ == '__main__':
    exit(main())
