#!/usr/bin/env python3
# -*- coding: utf-8-*-
"""\
Post CMIP6 Citation info from a JSON file.

---
THis script posts Citaion info to the citation service.

The JSON file can be obtained by getJSON.py, etc.

Without --do_post option, only check is done.


"""

from utils import loadJSON, postJSON
import json
import argparse

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

    parser.add_argument('--do_post',
                        dest='post', action='store_true',
                        help='do post JSON.',
                        default=False)

    parser.add_argument('jsonfile',
                        type=str,
                        help='filename to submit')

    return parser


def main():

    parser = my_parser()
    a = parser.parse_args()

    if (a.verbose):
        print('Configuration:')
        print('  do_post:',a.post)
        print('  JSON file:',a.jsonfile)

    d = loadJSON(a.jsonfile)

    if a.post:
        extra = None
    else:
        extra = 'check'
    status = postJSON(d, extra=extra)


    return 0

if __name__ == '__main__':
    exit(main())
