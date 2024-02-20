#!/usr/bin/env python

import sys
import pandas as pd
from glob import glob
from os import chdir
from os.path import isfile, abspath, dirname
import requests
from datetime import datetime

FILE=abspath(__file__)

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
    {FILE} /path/to/PHOENIX/PROTECTED/ API_TOKEN

Some PRESCIENT subjects are re-consonted between CHR & HC.
The prior consent stays in REDCap as a duplicate record.
This script deletes those records.''')
    exit(0)


with open('{}/bsub/rpms_records.txt'.format(dirname(FILE))) as f:
    dirs= f.read().strip().split()

ROOTDIR=sys.argv[1]
hashfile=f'{ROOTDIR}/date_offset.csv'
dhash=pd.read_csv(hashfile)
dhash.set_index('subject',inplace=True)

cleanfile=f'{ROOTDIR}/duplicate_arm.csv'
dclean=pd.read_csv(cleanfile)
dclean.set_index('subject',inplace=True)

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
        yp= df[df['version']=='YP']
        
        if len(yp)==0:
            print('\t','\033[0;31m YP\'s row absent in',inform_consent,'\033[0m \n')
            continue

        if yp['group'].unique().shape[0]==1:
            # this subject cannot have duplicate arm
            continue

        # to account for re-consent scenario, consider only the latest row
        yp_sorted= yp.sort_values('interview_date',
            key=lambda dates: [datetime.strptime(x,'%m/%d/%Y') for x in dates])
        chr_hc= yp_sorted.iloc[-1]['group']

    else:
        continue
    
    
    old=None
    

    # one try-except block to handle absence of incl_excl and empty chrcrit_part
    try:
        df= pd.read_csv(incl_excl)
        chrcrit_part= int(df['chrcrit_part'])

        if chrcrit_part==1:
            old=2
        elif chrcrit_part==2:
            old=1

    except (FileNotFoundError,ValueError):
        pass


    # if old arm was not determined in the previous block
    # try to determine it now from yp_sorted
    if not old:
        if yp['group'].unique().shape[0]>1:
            if chr_hc=='UHR':
                old=2
            elif chr_hc=='HealthyControl':
                old=1
        
    
    if old:

        ## skip if it was cleaned before ##
        try:
            assert (dclean.loc[subjectkey]==[old,1]).all()
            continue
        except (KeyError,AssertionError):
            pass
        
        
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

        try:
            r = requests.post('https://redcap.partners.org/redcap/api/',data=data)
            print('\t','HTTP Status: ' + str(r.status_code))
            if r.status_code!=200:
                print('\t',r.text,'\n')

            # set upload=1 so it can be re-downloaded
            # connect the setting with r.status_code so that
            # previously cleaned records are not re-downloaded
            if r.status_code==200 and dhash.loc[subjectkey,'upload']!=0:
                dhash.loc[subjectkey,'upload']=1
                dclean.loc[subjectkey]=old,1
                write=True
                

        except requests.exceptions.ConnectionError:
            print('\033[0;31m Remote disconnected, could not clean this subject \033[0m \n')
            

    chdir(ROOTDIR)


if write:
    dhash.reset_index(inplace=True)
    dhash.to_csv(hashfile,index=False)
    
    dclean.reset_index(inplace=True)
    dclean.to_csv(cleanfile,index=False)

print('\n\n')

