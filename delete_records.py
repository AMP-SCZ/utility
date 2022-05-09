#!/usr/bin/env python

from redcap_config import config
import requests
from glob import glob
from os import getenv
from os.path import basename, join as pjoin

data = {
    'token': config['api_token'],
    'action': 'delete',
    'content': 'record',
    'returnFormat': 'json'
}

redcap_phoenix= getenv('redcap_phoenix')
if redcap_phoenix:
    dirs= glob(pjoin(redcap_phoenix,'*/*/*'))
else:
    print("\"export redcap_phoenix=/path/to/PHOENIX/PROTECTED\", and try again")
    exit()

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

