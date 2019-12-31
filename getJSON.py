#!/usr/bin/env python3
# -*- coding: utf-8-*-
"""\
Get CMIP6 Citation info and save as a JSON file.

---
This script gets Citation info from the citation service.

You have to specify MIP(`activity_id`), model(`source_id`),
institution(`institution_id`), and experiment(`experiment_id`) to get
info.

"""
from utils import getJSON
import json
# import certifi
# import urllib3
import argparse

__author__ = 'T.Inoue'
__credits__ = 'Copyright (c) 2019 JAMSTEC'
__version__ = 'v20191213'
__date__ = '2019/12/13'


# mip = 'CMIP'
# model = 'MIROC6'
institution = 'MIROC'
# experiment = 'historical'

# mip = 'HighResMIP'
# model = 'NICAM16-7S'
# institution = 'MIROC'
# experiment = 'highresSST-present'

desc, epilog = __doc__.split('---')


def my_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc, epilog=epilog, )
    parser.add_argument('-v', '--verbose',
                        dest='verbose', action='store_true',
                        help='be verbose.',
                        default=False)
    parser.add_argument('-a', '--mip', '--activity_id',
                        type=str,
                        help='MIP(activity_id)',
                        default=None)
    parser.add_argument('-i', '--inst', '--institution_id',
                        metavar='inst', type=str,
                        help='inst(institution_id),default="%(default)s"',
                        default=institution)
    parser.add_argument('-s', '--model', '--source_id',
                        type=str,
                        help='model(source_id)',
                        default=None)
    parser.add_argument('-e', '--exp', '--experiment_id',
                        metavar='exp', type=str,
                        help='experiments to submit',
                        default=None)

    return parser


def main():

    parser = my_parser()
    a = parser.parse_args()

    if (a.verbose):
        print('Configuration:')
        print('  mip:', a.mip)
        print('  model:', a.model)
        print('  institution:', a.inst)
        print('  experiments:', a.exp)

    base = getJSON(source_id=a.model, activity_id=a.mip,
                   institution_id=a.inst, experiment_id=a.exp)
    if (base is None):
        parser.print_help()
        exit(1)

    base_title = base['titles'][0]
    base_subject = base['subjects'][0]['subject']

    if (a.verbose):
        print('base title:', base_title)
        print('base subject:', base_subject)

    fname = base_subject + '.json'
    with open(fname, 'w') as f:
        print('Saving base data to:', fname)
        json.dump(base, f, indent=2)
    print('Done.')

    return 0


if __name__ == '__main__':
    exit(main())
