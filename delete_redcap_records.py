#!/usr/bin/env python

import requests, sys
from glob import glob
from os import getenv
from os.path import abspath, basename, join as pjoin
import re
from time import sleep

if len(sys.argv)==1 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
{__file__} /path/to/PHOENIX/PROTECTED API_TOKEN
{__file__} /path/to/PHOENIX/PROTECTED API_TOKEN 1
The trailing 1 is for bulk removal of all records in the project.''')
    exit(0)

dirs= glob(pjoin(abspath(sys.argv[1]),'*/raw/*'))


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


cases= [basename(d) for d in dirs]

if len(sys.argv)==3:
    # serial removal
    for c in cases:
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


