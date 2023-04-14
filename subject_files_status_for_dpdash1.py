#!/usr/bin/env python

import json
from glob import glob
from os.path import isfile, abspath, basename, dirname, join as pjoin
import pandas as pd
import sys
from util import str_date_minus_str_date
from datetime import datetime

today=datetime.today().strftime('%Y-%m-%d')

def get_value(event,var):
    """Extract value from JSON"""

    for d in data1:
        if event in d['redcap_event_name']:
            try:
                if d[var]!='':
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
    if chreeg_interview_date=='':
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':'', 'eeg_missing':''}

    if get_value(timepoint,'chreeg_missing')=='1':
        missing_code=get_value(timepoint,'chreeg_missing_spec')
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':'', 'eeg_missing':missing_code}


    scan_minus_consent=str_date_minus_str_date(consent_date,chreeg_interview_date)
    days_since_scan=str_date_minus_str_date(chreeg_interview_date,today)
    
    # populate QC Score row
    # search for {site}-{subject}-EEGquick-day1to{scan_minus_consent+1} file
    try:
        score_file=pjoin(nda_root,network,
            f'PHOENIX/PROTECTED/{network}{site}/processed/{subject}/eeg/{site}-{subject}-EEGquick-day1to{scan_minus_consent+1}.csv')
        
        dfscore=pd.read_csv(score_file)
        eeg_score=dfscore.loc[0,'Rating']
        assert eeg_score>=1 and eeg_score<=4
    
    except:
        eeg_score=-days_since_scan


    # populate Data Transferred row
    # search for zip files
    _chreeg_interview_date=chreeg_interview_date.replace('-','')
    if isfile(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}{site}/raw/{subject}/eeg/{subject}_eeg_{_chreeg_interview_date}.zip')):
        eeg_data=1
    else:
        eeg_data=-days_since_scan


    # populate Protocol Followed row
    eeg_protocol=1
    for i in range(1,13):
        if get_value(timepoint,f'chreeg_run{i}')==3:
            eeg_protocol=0

    dict2={'eeg_score':eeg_score, 'eeg_data':eeg_data, 'eeg_protocol':eeg_protocol, 'eeg_date':chreeg_interview_date,
        'eeg_missing':''}

    return dict2


def get_avl_status():
    chreeg_interview_date=get_value(timepoint,'chrspeech_interview_date')
    if chreeg_interview_date=='':
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':'', 'eeg_missing':''}

    if get_value(timepoint,'chrspeech_missing')=='1':
        missing_code=get_value(timepoint,'chrspeech_missing_spec')
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':'', 'eeg_missing':missing_code}


    scan_minus_consent=str_date_minus_str_date(consent_date,chreeg_interview_date)
    days_since_scan=str_date_minus_str_date(chreeg_interview_date,today)
    
    # populate QC Score row
    # search for {site}-{subject}-EEGquick-day1to{scan_minus_consent+1} file
    try:
        score_file=pjoin(nda_root,'AVL_quick_qc/open_count/{site}-{subject}-open_count-day1to*.csv')
        
        dfscore=pd.read_csv(score_file[0])

        for i,row in dfscore.iterrows():
            if row['timepoint']==int(scan_minus_consent)+1:
                eeg_score=row['audio_quality_category']
 
    except:
        eeg_score=-days_since_scan


    # populate Data Transferred row
    # search for zip files
    _chreeg_interview_date=chreeg_interview_date.replace('-','')
    prefix=pjoin(nda_root,network,f'PHOENIX/GENERAL/{network}??/processed/{subject}/interviews/open/')

    eeg_data=1
    for suffix in [f'interviewRedactedTranscriptQC_open-day*to{_chreeg_interview_date}.csv',
        f'interviewMonoAudioQC_open-day*to{_chreeg_interview_date}.csv',
        f'interviewVideoQC_open-day*to{_chreeg_interview_date}.csv']:
        
        if len(glob(prefix+suffix))!=1
            eeg_data=0
            eeg_data=-days_since_scan
            break


    # populate Protocol Followed row
    eeg_protocol=1
    if get_value(timepoint,'chrspeech_deviation')=='0' or get_value(timepoint,'chrspeech_quality')=='0':
        eeg_protocol=0


    dict2={'eeg_score':eeg_score, 'eeg_data':eeg_data, 'eeg_protocol':eeg_protocol, 'eeg_date':chreeg_interview_date,
        'eeg_missing':''}

    return dict2



if __name__=='__main__':

    nda_root='/data/predict1/data_from_nda/'
    network='Pronet'
    timepoint='baseline'

    outdir=pjoin(nda_root,f'{network}_status')

    surveys=glob(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}??/raw/*/surveys/*.{network}.json'))


    # initiate DataFrame
    df1=pd.DataFrame(columns=['day,reftime,timeofday,weekday,subject_id,site'.split(',')])

    for s in surveys:
        
        print('processing',s)

        with open(s) as f:
            data1=json.load(f)

        consent_date=get_value('screening','chric_consent_date')

        # extract and join CHR and HC arms
        data=[]
        for d in data1:
            if timepoint in d['redcap_event_name']:
                data.append(d)
        data1=data

        subject=basename(s).split('.')[0]
        site=subject[:2]

        # initialize dict
        dict_all={'day':[1],'reftime':'','timeofday':'','weekday':'',
            'site':site,'subject_id':subject}

        
        # populate MRI block
        # dict_mri=get_mri_status()
            
        # populate EEG block
        # dict_eeg=get_eeg_status()

        # populate A/V/L block
        dict_avl=get_avl_status()


        # join the dicts
        # dict_all.update(dict_mri)
        # dict_all.update(dict_eeg)
        dict_all.update(dict_avl)

        # transform to DataFrame
        df=pd.DataFrame(dict_all)

        # write out subject DataFrame
        outfile=pjoin(outdir,f'{site}-{subject}-data_{timepoint}-day1to1.csv')
        df.to_csv(outfile,index=False)
    
    
