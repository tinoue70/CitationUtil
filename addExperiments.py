#!/usr/bin/env python3
# -*- coding: utf-8-*-

"""\
Create CMIP6 Citation info of experiment granularity.

---
This script gets base (MIP-granularity) info from the citation service
or local JSON file, adds experiment informations.

Use modJSON.py to modify creator list, if needed.

Use postJSON.py to check/post created JSON file.

You have to specify MIP(`activity_id`), model(`source_id`) to get base
info, and have to specify experiments(`experiment_id`) to submit
experiment-granularity info.
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
    parser.add_argument('experiments',
                        metavar='exp', type=str, nargs='*',
                        help='experiments to submit')
    parser.add_argument('-a', '--mip', '--activity_id',
                        type=str,
                        help='MIP(activity_id)',
                        default=mip)
    parser.add_argument('-i', '--inst', '--institution_id',
                        type=str,
                        help='institution(institution_id)',
                        default=inst)
    parser.add_argument('-s', '--model', '--source_id',
                        type=str,
                        help='model(source_id)',
                        default=model)

    parser.add_argument('-l', '--loadfile',
                        type=str,
                        help='Load base JSON from local file', nargs='?',
                        default=None, const='')
    return parser


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


def main():

    parser = my_parser()
    a = parser.parse_args()

    if (a.verbose):
        print('Configuration:')
        # print('  dopost:', a.dopost)
        print('  model:', a.model)
        print('  mip:', a.mip)
        print('  experiments:', a.experiments)
        if (a.loadfile is None):
            print('  loadfile: not specified')
        elif (a.loadfile):
            print('  loadfile: specified explicitly:', a.loadfile)
        else:
            a.loadfile = setJSONfname(source_id=a.model, activity_id=a.mip,
                                      institution_id=a.inst)
            print('  loadfile: set as:', a.loadfile)

    if (a.loadfile is None):
        base = getJSON(source_id=a.model, activity_id=a.mip,
                       institution_id=a.inst)
    else:
        if (a.verbose):
            print('file:', a.loadfile)
        base = loadJSON(a.loadfile)

    if (base is None):
        exit(1)

    base_title = base['titles'][0]
    base_subject = base['subjects'][0]['subject']

    if (a.verbose):
        print('base title:', base_title)
        print('base subject:', base_subject)

    for exp in a.experiments:
        data = addExperiment(base, exp)     # base is preserved.
        data_title = data['titles'][0]
        data_subject = data['subjects'][0]['subject']
        if (a.verbose):
            print('data title:', data_title)
            print('data subject:', data_subject)
        # print(data)
        fname = setJSONfname(a.model, a.mip, a.inst, exp)
        with open(fname, 'w') as f:
            print('Saving base data to:', fname)
            json.dump(data, f, indent=2)
    print('Done.')

    return 0


if __name__ == '__main__':
    exit(main())
