#!/usr/bin/env python

import sys
import pandas as pd
from glob import glob
from os import chdir
from os.path import isfile
import requests


with open('/data/predict1/utility/bsub/rpms_records.txt') as f:
    dirs= f.read().strip().split()

ROOTDIR=sys.argv[1]
hashfile=f'{ROOTDIR}/date_offset.csv'
dhash=pd.read_csv(hashfile)
dhash.set_index('subject',inplace=True)

print('\n\n')

write=False
for dir in dirs:

    ## old arm detection block ##

    # print(dir)
    chdir(ROOTDIR+'/'+dir)
    subjectkey= dir.split('/')[2]

    incl_excl= subjectkey+ '_inclusionexclusion_criteria_review.csv'
    inform_consent= subjectkey+ '_informed_consent_run_sheet.csv'

    if isfile(inform_consent):
        df= pd.read_csv(inform_consent)
        # extract Young Patient's rows only, we do not need Guardian's rows
        yp_rows= df[df['version']=='YP']
        _chr_hc= yp_rows['group'].unique()
        # to account for re-consent scenario, consider only the last row
        chr_hc= yp_rows.iloc[-1]['group']

    else:
        continue
    
    
    old=None

    # one try-except block to handle absence of incl_excl and empty chrcrit_part
    try:
        df= pd.read_csv(incl_excl)
        chrcrit_part= int(df['chrcrit_part'])

        if chrcrit_part==1 and chr_hc=='HealthyControl':
            old=2
        elif chrcrit_part==2 and chr_hc=='UHR':
            old=1

    except (FileNotFoundError,ValueError):
        # determine old arm, if any, through yp_rows
        pass

    if len(_chr_hc)>1:
        if chr_hc=='UHR':
            old=2
        elif chr_hc=='HealthyControl':
            old=1
        
    if old:
        print(dir)
        old=f'{old}'
        print(f'old arm:',old)


        ## old arm cleanup block ##
        data = {
            'token': sys.argv[2],
            'action': 'delete',
            'content': 'record',
            'records[0]': subjectkey,
            'arm': old,
            'returnFormat': 'json'
        }
        #r = requests.post('https://redcap.partners.org/redcap/api/',data=data)
        #print('HTTP Status: ' + str(r.status_code))
        #print(r.text)


        # set upload=1 so it can be re-downloaded
        if dhash.loc[subjectkey,'upload']!=1:
            dhash.loc[subjectkey,'upload']=1
            write=True
    


    chdir(ROOTDIR)


if write:
    dhash.reset_index(inplace=True)
    dhash.to_csv(hashfile,index=False)

print('\n\n')

