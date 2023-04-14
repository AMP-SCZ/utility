#!/bin/bash

import json
from glob import glob
from os.path import abspath, basename, dirname, join as pjoin
import pandas as pd
import sys
from util import str_date_minus_str_date
from datetime import datetime

today=datetime.today().strftime('%Y-%m-%d')

def get_value(var,event):
    """Extract value from JSON"""

    for d in dict1:
        if timepoint in d['redcap_event_name']:
            try:
                return d[var]
            except KeyError:
                pass
                
    # the subject has not reached the event yet
    return ''



def get_mri_status():
    """Available variables:

    nda_root
    network
    timepoint
    s: JSON path
    data: two-element JSON array of timepoint of CHR and HC arms
    consent_date
    site
    subject
    """
    
    chrmri_entry_date=get_value(timepoint,'chrmri_entry_date')
    scan_minus_consent=str_date_minus_str_date(consent_date,chreeg_interview_date)
    days_since_scan=str_date_minus_str_date(chreeg_interview_date,today)


    pass

    # return a dictionary of {MRI QC Score, Data Transferred, Protocol Followed, Acquisition Date}


def get_eeg_status():

    chreeg_interview_date=get_value(timepoint,'chreeg_interview_date')

    scan_minus_consent=str_date_minus_str_date(consent_date,chreeg_interview_date)
    days_since_scan=str_date_minus_str_date(chreeg_interview_date,today)
    
    # populate QC Score row
    # search for {site}-{subject}-EEGquick-day1to{scan_minus_consent+1} file
    try:
        score_file=pjoin(nda_root,network,
            f'PHOENIX/PROTECTED/{network}??/*/processed/*/eeg/{site}-{subject}-EEGquick-day1to{scan_minus_consent+1}.csv')
        
        dfscore=pd.read_csv(score_file)
        assert dfscore['Rating']>=1 and dfscore['Rating']<=4
        eeg_score=dfscore.loc[0,'Rating']

    except:
        eeg_score=-days_since_scan


    # populate Data Transferred row
    # search for zip files
    if isfile(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}??/raw/*/eeg/{subject}_eeg_{chreeg_interview_date.replace('-','')}.zip'))
        eeg_data=1
    else:
        eeg_data=-days_since_scan


    # populate Protocol Followed row
    run=0
    for i in range(1,13):
        run+=int(get_value(timepoint,f'chreeg_run{i}'))

    if run<12:
        eeg_protocol=0
    else:
        eeg_protocol=1


    dict2={'eeg_score':eeg_score, 'eeg_data':eeg_data, 'eeg_protocol':eeg_protocol, 'eeg_date':chreeg_interview_date}

    return dict2


def get_avl_status():
    pass






if __name__=='__main__':

    nda_root='/data/predict1/data_from_nda/'
    network='Pronet'
    timepoint='baseline'

    outdir=pjoin(nda_root,f'{network}_status')

    surveys=glob(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}??/raw/*/surveys/*.{network}.json'))


    # initiate DataFrame
    df1=pd.DataFrame(columns=['day,reftime,timeofday,weekday,subject_id,site'.split(',')])

    for s in surveys:

        with open(s) as f:
            data1=json.load(f.read())


        # extract and join CHR and HC arms
        data=[]
        for d in data:
            if timepoint in d['redcap_event_name']:
                data.append(d)


        subject=basename(s).split('.')[0]
        site=subject[:2]

        # initialize dict
        dict_all={'day':1,'reftime':'','timeofday':'','weekday':'',
            'site':site,'subject_id':subject}

        
        consent_date=get_value('screening','chric_consent_date')

        # populate MRI block
        # dict_mri=get_mri_status()
            
        # populate EEG block
        dict_eeg=get_eeg_status()

        # populate A/V/L block
        # dict_avl=get_avl_status()


        # join the dicts
        dict_all.update(dict_mri)
        dict_all.update(dict_eeg)
        dict_all.update(dict_avl)

        # transform to DataFrame
        df=pd.DataFrame(dict_all)

        # write out subject DataFrame
        outfile=pjoin(outdir,f'{site}-{subject}-data_{timepoint}.day1to1.csv')
        df.to_csv(outfile,index=False)
    
    
