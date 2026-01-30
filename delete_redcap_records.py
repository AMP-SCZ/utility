#!/usr/bin/env python

import requests, sys
from glob import glob
from os import getenv
from os.path import abspath, basename, join as pjoin, split as psplit
import re
from time import sleep

if len(sys.argv)==1 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
{__file__} /path/to/PHOENIX/PROTECTED API_TOKEN
{__file__} /path/to/PHOENIX/PROTECTED API_TOKEN 1
{__file__} /path/to/PHOENIX/PROTECTED/PresientBM/raw/BM12345 API_TOKEN
{__file__} /path/to/PHOENIX/PROTECTED/PresientBM/raw/BM12345/surveys API_TOKEN
{__file__} /path/to/PHOENIX/PROTECTED/PresientBM/raw/BM12345/surveys/BM12345.Prescient.json API_TOKEN
The trailing 1 is for bulk removal of all records in the project.''')
    exit(0)

if sys.argv[1].rstrip('/').endswith('PROTECTED'):
    # multiple records
    dirs= glob(pjoin(abspath(sys.argv[1]),'*/raw/*'))
    cases= [basename(d) for d in dirs]

else:
    # single record
    s= re.search('[A-Z]{2}[0-9]{5}',sys.argv[1])
    if not s:
        print('No record ID could be extracted from', sys.argv[1])
        exit()
    cases= [s.group()]


def construct(_cases):

    data = {
        'token': sys.argv[2],
        'action': 'delete',
        'content': 'record',
        'returnFormat': 'json'
    }

    for i,c in enumerate(_cases):
        data[f'records[{i}]']= c

    return data


def POST(_data):
    
    try:
        r = requests.post('https://redcap.partners.org/redcap/api/',data=_data)
        print('HTTP Status: ' + str(r.status_code))
        print(r.text)
    except requests.exceptions.ConnectionError:
        print('requests.exceptions.ConnectionError occurred, retrying after 30 seconds')
        sleep(30)
        POST(_data)

    return r


if len(sys.argv)==3:
    # serial removal
    for c in cases:
        print('Delete',c)
        data= construct([c])
        POST(data)

elif len(sys.argv)==4 and sys.argv[3]=='1':
    # bulk removal
    while 1:
        data= construct(cases)
        r= POST(data)

        if r.status_code==400:
            non_existent=re.findall('[A-Z][A-Z]\d{5}',r.text)
            for s in non_existent:
                cases.remove(s)
        
        elif r.status_code==200:
            break


