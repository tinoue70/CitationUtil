#!/usr/bin/env python3
# -*- coding: utf-8-*-
"""\
Modify "Creators" in CMIP6 Citation info JSON file.

---
This script reads and modifies "Creators" in Citaion info JSON file.
New list is read from an excel file,

The JSON file can be obtained by getJSON.py, etc.
"""

from utils import loadJSON, postJSON, Creator
import json
import argparse
from copy import deepcopy
import pandas as pd
from pprint import pprint

__author__ = 'T.Inoue'
__credits__ = 'Copyright (c) 2019 JAMSTEC'
__version__ = 'v20191229'
__date__ = '2019/12/29'

desc, epilog = __doc__.split('---')

def my_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc, epilog=epilog, )

    parser.add_argument('-v', '--verbose',
                        dest='verbose', action='store_true',
                        help='be verbose.',
                        default=False)

    parser.add_argument('-s', '--save',
                        action='store_true',
                        help='save modified JSON.',
                        default=False)

    parser.add_argument('--do_post',
                        dest='post', action='store_true',
                        help='Do POST modified JSON',
                        default=False)

    parser.add_argument('jsonfile',
                        type=str,
                        help='json file to be modified')

    parser.add_argument('excelfile',
                        type=str,
                        help='excel file of substitution list')

    return parser


def loadCreators(xlsfile, mip, exp):
    if exp:
        df = pd.read_excel(xlsfile, sheet_name='Exp')
    else:
        df = pd.read_excel(xlsfile, sheet_name='MIP')

    if exp == None:
        exp = 'NaN'

    q_str = f"MIP == '{mip}' and experiment == '{exp}'"
    print(q_str)
    l = df.query(q_str)
    c_list = l['creators'].values[0].split('\n')

    creators = []
    # print(len(c_list))
    for c_txt in c_list:
        print(c_txt)
        fullname, email, aff = [x.strip() for x in c_txt.split(',',2)]
        # print(f'"{fullname}"\t"{email}"\t "{aff}"')
        creators.append(
            Creator(fullName=fullname, email=email, affiliation=aff).toJSON())

    return creators


def main():
    parser = my_parser()
    a = parser.parse_args()

    if (a.verbose):
        print('Configuration:')
        print('  JSON file:',a.jsonfile)
        print('  Save:',a.save)
        print('  Excel file:',a.excelfile)
        print('  DoPost:', a.post)

    orig_json = loadJSON(a.jsonfile)
    orig_creators = orig_json['creators']
    print('Original creators:')
    for c in orig_creators:
        print(f"+ {c['creatorName']}\t{c['email']}\t{c['affiliation']}")

    # pprint(orig_json.keys())
    subject = orig_json['subjects'][0]['subject']
    title = orig_json['titles'][0]
    ( era, mip, inst, model ) = subject.split('.', 3)
    try:
        (model, exp) = model.split('.')
    except ValueError:
        exp = None

    print('Loaded JSON:')
    print('  subject:', subject)
    print('  title:', title)
    print('  mip:', mip)
    print('  model:', model)
    print('  exp:', exp)

    new_creators = loadCreators(a.excelfile, mip, exp)
    print('New creators:')
    for c in new_creators:
        print(f"+ {c['creatorName']}\t{c['email']}\t{c['affiliation']}")

    new_json = deepcopy(orig_json)
    new_json['creators'] = new_creators

    if (a.post):
        extra = ''
    else:
        extra = 'check'

    if (a.save):
        with open(a.jsonfile, 'w') as f:
            json.dump(new_json, f, indent=4)
    else:
        status = postJSON(new_json, extra)
        print(status)


    return 0


if __name__ == '__main__':
    exit(main())
    
