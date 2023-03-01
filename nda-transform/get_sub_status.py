#!/usr/bin/env python

import json
import requests
from os import getenv
import argparse

parser= argparse.ArgumentParser("Get info of NDA submissions")
parser.add_argument('-u','--user', required=True,
    help="NDA download manager username (different from login.gov credential)")
parser.add_argument('-p','--password', required=True,
    help="NDA download manager password (different from login.gov credential)")

args=parser.parse_args()

# user=getenv('DOWNLOAD_MANAGER_USER')
# password=getenv('DOWNLOAD_MANAGER_PASSWORD')


req_string=f"https://{args.user}:{args.password}@nda.nih.gov/api/submission/"

r = requests.get(req_string)
print('HTTP Status: ' + str(r.status_code))

dict1=r.json()

for i,d in enumerate(dict1):
    print('{:2d} {} {:4s} {} {:16.16s} {:.40s}'.format(
        i+1,d['submission_id'],d['collection']['id'],d['dataset_created_date'][:16],d['submission_status'],d['dataset_title']))


