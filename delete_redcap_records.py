#!/usr/bin/env python

import requests, sys
from glob import glob
from os import getenv
from os.path import abspath, basename, join as pjoin

if len(sys.argv)==1 or sys.argv[1] in ['-h','--help']:
    print('''Usage: /path/to/delete_records.py /path/to/PHOENIX/PROTECTED API_TOKEN''')
    exit(0)

dirs= glob(pjoin(abspath(sys.argv[1]),'*/raw/*'))

data = {
    'token': sys.argv[2],
    'action': 'delete',
    'content': 'record',
    'returnFormat': 'json'
}

cases= [basename(d) for d in dirs]

# for serial removal
for i,c in enumerate(cases):
    data['records[0]']= c
    r = requests.post('https://redcap.partners.org/redcap/api/',data=data)
    print('HTTP Status: ' + str(r.status_code))
    print(r.text)


# for bulk removal
# for i,c in enumerate(cases):
#     data[f'records[{i}]']= c
# r = requests.post('https://redcap.partners.org/redcap/api/',data=data)
# print('HTTP Status: ' + str(r.status_code))
# print(r.text)

