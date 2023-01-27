#!/usr/bin/env python

import pandas as pd
import json
from os import getcwd, chdir
from os.path import dirname, basename, abspath
import sys
from glob import glob
from multiprocessing import Pool
import signal
import requests


# Download PRESCIENT records from MGB REDCap
# Usage:
# __file__ PHOENIX_PROTECTED API_TOKEN
# __file__ PHOENIX_PROTECTED API_TOKEN 16
# API TOKEN for the REDCap project to pull records from
# optional: 16 is for ncpu



dir_bak=getcwd()
chdir(sys.argv[1])

try:
    df=pd.read_csv('date_offset.csv')
    subjects=df['subject'].values
    force=0
except:
    subjects= [p.split('/')[-1] for p in glob("*/raw/*")]
    force=1


def RAISE(err):
    raise err


def _shift_date(sub):
    
    if force==0 and df.loc[sub,'upload']==0:
        return
        
    json_file=f'Prescient{sub[:2]}/raw/{sub}/surveys/{sub}.Prescient.json'
            
    # make API call
    data = {
        'token': sys.argv[2],
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'records[0]': sub,
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    
    r = requests.post('https://redcap.partners.org/redcap/api/',data=data)
    print('HTTP Status: ' + str(r.status_code))
    
    if r.status_code=='200':
        # success
        with open(json_file, 'w') as f:
            json.dump(r.json(),f)
    else:
        # failure
        print(r.json())



if len(sys.argv)==3:
    ncpu=int(sys.argv[3])
else:
    ncpu=16

if ncpu==1:
    # useful for debugging
    for sub in subjects:
        _down_record(sub)
else:
    sigint_handler= signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool= Pool(ncpu)
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        pool.map_async(_down_record, subjects, error_callback=RAISE)
    except KeyboardInterrupt:
        pool.terminate()
    else:
        pool.close()
    pool.join()


chdir(dir_bak)


