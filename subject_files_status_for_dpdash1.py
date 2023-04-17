#!/usr/bin/env python

import json
from glob import glob
from os.path import isfile, abspath, basename, dirname, join as pjoin
import pandas as pd
import sys
from util import str_date_minus_str_date
from datetime import datetime

today=datetime.today().strftime('%Y-%m-%d')
df_mri=pd.read_csv('/data/predict1/data_from_nda/MRI_ROOT/eeg_mri_count/mri_all_db.csv')
df_mri.set_index('subject',inplace=True)

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
    

    chreeg_interview_date=get_value(timepoint,'chrmri_entry_date')
    if chreeg_interview_date=='':
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':'', 'eeg_missing':''}

    if get_value(timepoint,'chrmri_missing')=='1':
        missing_code=get_value(timepoint,'chrmri_missing_spec')
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':chreeg_interview_date, 'eeg_missing':missing_code}

    scan_minus_consent=str_date_minus_str_date(consent_date,chreeg_interview_date)
    days_since_scan=str_date_minus_str_date(chreeg_interview_date,today)+1

    
    eeg_score=-days_since_scan
    eeg_data=-days_since_scan

    try:
        for s,row in df_mri.loc[subject].iterrows():
            if timepoint in row['timepoint_text']:
                break
                
    except:
        pass


    try:
        eeg_score=int(row['mriqc_int'])
        assert eeg_score>=0 and eeg_score<=4

    except:
        pass
    
    try:
        eeg_data=int(row['mri_data_exist'])
    except:
        pass
    

    eeg_protocol=1

    for v in ['chrmri_confirm','chrmri_consent',
        'chrmri_metal','chrmri_physicalmetal']:

        if get_value(timepoint,v)!='1':
            eeg_protocol=0
            break

    if get_value(timepoint,'chrmri_dental')=='1':
        eeg_protocol=0

    for v in ['chrmri_aahscout',
            'chrmri_calib_ge', 'chrmri_calib_ge_2', 'chrmri_calib_ge_3',
            'chrmri_localizeraligned', 'chrmri_localizerseq',
            'chrmri_localizerseq_ge',
            'chrmri_dmap', 'chrmri_dmap2', 'chrmri_dmap3',
            'chrmri_dmap_qc', 'chrmri_dmap_qc_2', 'chrmri_dmap_qc_3',
            'chrmri_dmpa', 'chrmri_dmpa2', 'chrmri_dmpa3',
            'chrmri_dmpa_qc', 'chrmri_dmpa_qc_2', 'chrmri_dmpa_qc_3',
            'chrmri_t1', 'chrmri_t1_qc',
            'chrmri_t2', 'chrmri_t2_qc', 'chrmri_t2_ge', 'chrmri_t2_qc_ge',
            'chrmri_dmri126', 'chrmri_dmri126_qc',
            'chrmri_dmri176', 'chrmri_dmri176_qc',
            'chrmri_dmri_b0', 'chrmri_dmri_b0_2',
            'chrmri_dmri_b0_qc', 'chrmri_dmri_b0_qc_2',
            'chrmri_rfmriap', 'chrmri_rfmriap2',
            'chrmri_rfmriap2_qc', 'chrmri_rfmriap_qc',
            'chrmri_rfmriap_ref_num', 'chrmri_rfmriap_ref_num_2',
            'chrmri_rfmriap_ref_qc', 'chrmri_rfmriap_ref_qc_2',
            'chrmri_rfmripa', 'chrmri_rfmripa2',
            'chrmri_rfmripa2_qc', 'chrmri_rfmripa_qc',
            'chrmri_rfmripa_ref_num', 'chrmri_rfmripa_ref_num_2',
            'chrmri_rfmripa_ref_qc', 'chrmri_rfmripa_ref_qc_2']:
    
        if get_value(timepoint,v)=='3':
            eeg_protocol=0
            break


    dict2={'mri_score':eeg_score, 'mri_data':eeg_data, 'mri_protocol':eeg_protocol, 'mri_date':chreeg_interview_date,
        'mri_missing':''}

    return dict2




def get_eeg_status():

    chreeg_interview_date=get_value(timepoint,'chreeg_interview_date')
    if chreeg_interview_date=='':
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':'', 'eeg_missing':''}

    if get_value(timepoint,'chreeg_missing')=='1':
        missing_code=get_value(timepoint,'chreeg_missing_spec')
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':chreeg_interview_date, 'eeg_missing':missing_code}


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
    eeg_data=1
    if eeg_score==-days_since_scan:
        _chreeg_interview_date=chreeg_interview_date.replace('-','')
        if not isfile(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}{site}/raw/{subject}/eeg/{subject}_eeg_{_chreeg_interview_date}.zip')):
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
        return {'avl_score':'', 'avl_data':'', 'avl_protocol':'', 'avl_date':'', 'avl_missing':''}

    if get_value(timepoint,'chrspeech_missing')=='1':
        missing_code=get_value(timepoint,'chrspeech_missing_spec')
        return {'avl_score':'', 'avl_data':'', 'avl_protocol':'', 'avl_date':chreeg_interview_date, 'avl_missing':missing_code}


    scan_minus_consent=str_date_minus_str_date(consent_date,chreeg_interview_date)
    scan_minus_consent=int(scan_minus_consent)+1
    days_since_scan=str_date_minus_str_date(chreeg_interview_date,today)
    
    # populate QC Score row
    eeg_score=-days_since_scan
    try:
        score_file=pjoin(nda_root,f'AVL_quick_qc/open_count/{site}-{subject}-open_count-day1to*.csv')
        score_file=glob(score_file)

        dfscore=pd.read_csv(score_file[0])

        for i,row in dfscore.iterrows():
            if row['timepoint']==scan_minus_consent:
                eeg_score=row['audio_quality_category']
        
        assert eeg_score>=1 and eeg_score<=5

    except:
        pass


    # populate Data Transferred row
    # search for zip files
    _chreeg_interview_date=chreeg_interview_date.replace('-','')
    prefix=pjoin(nda_root,network,f'PHOENIX/GENERAL/{network}??/processed/{subject}/interviews/open/')


    eeg_data=1
    # if there is a valid score, data is surely here
    if eeg_score==-days_since_scan:

        if len(glob(prefix+ '*interview*_open-day*to*.csv'))<2:
            eeg_data=-days_since_scan
        
        # following could be a stricter way to detect data availability
        '''
        for desc in ['interviewRedactedTranscriptQC_open','interviewMonoAudioQC_open','interviewVideoQC_open']:

            pattern= prefix+ '*'+ desc+ f'-day*to{scan_minus_consent}.csv'
            if len(glob(pattern))!=1:
                eeg_data=-days_since_scan
                break
        '''


    # populate Protocol Followed row
    eeg_protocol=1
    if get_value(timepoint,'chrspeech_deviation')=='0' or get_value(timepoint,'chrspeech_quality')=='0':
        eeg_protocol=0


    dict2={'avl_score':eeg_score, 'avl_data':eeg_data, 'avl_protocol':eeg_protocol, 'avl_date':chreeg_interview_date,
        'avl_missing':''}

    return dict2


def get_cnb_status():

    chreeg_interview_date=get_value(timepoint,'chrpenn_interview_date')
    if chreeg_interview_date=='':
        return {'cnb_data':'', 'cnb_protocol':'', 'cnb_date':'', 'cnb_missing':''}

    if get_value(timepoint,'chrpenn_missing')=='1':
        missing_code=get_value(timepoint,'chrpenn_missing_spec')
        return {'cnb_data':'', 'cnb_protocol':'', 'cnb_date':chreeg_interview_date, 'cnb_missing':missing_code}


    scan_minus_consent=str_date_minus_str_date(consent_date,chreeg_interview_date)
    days_since_scan=str_date_minus_str_date(chreeg_interview_date,today)
    

    # populate Data Transferred row
    # search for zip files
    eeg_data=1
    if not isfile(s.replace('.Pronet.json','.UPENN.json')):
        eeg_data=-days_since_scan


    # populate Protocol Followed row
    eeg_protocol=1
    if get_value(timepoint,f'chrpenn_complete')!='0':
        eeg_protocol=0

    dict2={'cnb_data':eeg_data, 'cnb_protocol':eeg_protocol, 'cnb_date':chreeg_interview_date,
        'cnb_missing':''}

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
        dict_mri=get_mri_status()
            
        # populate EEG block
        dict_eeg=get_eeg_status()

        # populate A/V/L block
        dict_avl=get_avl_status()

        # populate CNB block
        dict_cnb=get_cnb_status()

        # join the dicts
        dict_all.update(dict_mri)
        dict_all.update(dict_eeg)
        dict_all.update(dict_avl)
        dict_all.update(dict_cnb)

        # transform to DataFrame
        df=pd.DataFrame(dict_all)

        # write out subject DataFrame
        outfile=pjoin(outdir,f'{site}-{subject}-data_{timepoint}-day1to1.csv')
        df.to_csv(outfile,index=False)
    
    
