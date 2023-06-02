#!/usr/bin/env python

import json
from glob import glob
from os.path import isfile, abspath, basename, dirname, join as pjoin
import pandas as pd
import sys
from util import str_date_minus_str_date
from datetime import datetime
import argparse

today=datetime.today().strftime('%Y-%m-%d')
df_mri=pd.read_csv('/data/predict1/data_from_nda/MRI_ROOT/eeg_mri_count/mri_all_db.csv')
df_mri.set_index('subject',inplace=True)

def get_value(event,var):
    """Extract value from JSON"""

    for d in dict1:
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
    

    interview_date=get_value(timepoint,'chrmri_entry_date')
    if interview_date=='':
        return {'mri_score':'', 'mri_data':'', 'mri_protocol':'', 'mri_date':'', 'mri_missing':''}

    if get_value(timepoint,'chrmri_missing')=='1':
        missing_code=get_value(timepoint,'chrmri_missing_spec')
        return {'mri_score':'', 'mri_data':'', 'mri_protocol':'', 'mri_date':interview_date, 'mri_missing':missing_code}

    scan_minus_consent=str_date_minus_str_date(consent_date,interview_date)
    days_since_scan=str_date_minus_str_date(interview_date,today)
    

    try:
        for s,row in df_mri.loc[subject].iterrows():
            if timepoint in row['timepoint_text']:
                break
    
    except (KeyError,AttributeError,TypeError):
        # KeyError: subject does not exist in df_mri
        # AttributeError: only one row for the subject
        # TypeError: timepoint_text cell is NaN for the subject
        
        try:
            row=df_mri.loc[subject]
        except (KeyError,TypeError):
            pass


    try:
        score=int(row['mriqc_int'])
        assert score>=0 and score<=2
        # 0: unusable, 1: partial pass, 2: full pass
    except:
        score=-days_since_scan
    
    try:
        data=int(row['mri_data_exist'])
        assert data==1
    except:
        data=-days_since_scan
        
    
    protocol=1

    for v in ['chrmri_consent','chrmri_metal','chrmri_physicalmetal']:
        if get_value(timepoint,v)!='1':
            protocol=0
            break

    if get_value(timepoint,'chrmri_confirm')=='2':
        protocol=0

    if get_value(timepoint,'chrmri_dental')=='1':
        protocol=0

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
            protocol=0
            break


    dict2={'mri_score':score, 'mri_data':data, 'mri_protocol':protocol, 'mri_date':interview_date,
        'mri_missing':''}

    return dict2



def get_eeg_status():

    interview_date=get_value(timepoint,'chreeg_interview_date')
    if interview_date=='':
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':'', 'eeg_missing':''}

    if get_value(timepoint,'chreeg_missing')=='1':
        missing_code=get_value(timepoint,'chreeg_missing_spec')
        return {'eeg_score':'', 'eeg_data':'', 'eeg_protocol':'', 'eeg_date':interview_date, 'eeg_missing':missing_code}


    scan_minus_consent=str_date_minus_str_date(consent_date,interview_date)
    days_since_scan=str_date_minus_str_date(interview_date,today)
    
    # populate QC Score row
    # search for {site}-{subject}-EEGquick-day1to{scan_minus_consent} file
    try:
        score_file=pjoin(nda_root,network,
            f'PHOENIX/PROTECTED/{network}{site}/processed/{subject}/eeg/{site}-{subject}-EEGquick-day1to{scan_minus_consent}.csv')
        
        dfscore=pd.read_csv(score_file)
        score=dfscore.loc[0,'Rating']
        assert score>=1 and score<=4
        # 1: poor, 2: average, 3: good, 4: excellent
    
    except:
        score=-days_since_scan


    # populate Data Transferred row
    # search for zip files
    data=1
    if score==-days_since_scan:
        _interview_date=interview_date.replace('-','')
        if not isfile(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}{site}/raw/{subject}/eeg/{subject}_eeg_{_interview_date}.zip')):
            data=-days_since_scan


    # populate Protocol Followed row
    protocol=1
    for i in range(1,13):
        if get_value(timepoint,f'chreeg_run{i}')==3:
            protocol=0

    dict2={'eeg_score':score, 'eeg_data':data, 'eeg_protocol':protocol, 'eeg_date':interview_date,
        'eeg_missing':''}

    return dict2



def get_avl_status():
    
    interview_date=get_value(timepoint,'chrspeech_interview_date')
    if interview_date=='':
        return {'avl_score':'', 'avl_data':'', 'avl_protocol':'', 'avl_date':'', 'avl_missing':''}

    if get_value(timepoint,'chrspeech_missing')=='1':
        missing_code=get_value(timepoint,'chrspeech_missing_spec')
        return {'avl_score':'', 'avl_data':'', 'avl_protocol':'', 'avl_date':interview_date, 'avl_missing':missing_code}


    scan_minus_consent=str_date_minus_str_date(consent_date,interview_date)
    days_since_scan=str_date_minus_str_date(interview_date,today)
    
    # populate QC Score row
    try:
        score_file=pjoin(nda_root,f'AVL_quick_qc/open_count/{site}-{subject}-open_count-day1to*.csv')
        score_file=glob(score_file)

        dfscore=pd.read_csv(score_file[0])
        
        # find the nearest day number among dfscore['timepoint']
        min_diff=9999
        for d in dfscore['timepoint'].values:
            diff=abs(d-scan_minus_consent)
            if diff<min_diff:
                min_diff=diff
                nearest_day=d
        
        for i,row in dfscore.iterrows():
            if row['timepoint']==nearest_day:
                score=row['audio_quality_category']
                
        assert score>=1 and score<=5
        # 1: excellent, 2: good, 3: fair, 4: usable, 5: bad

    except:
        score=-days_since_scan


    # populate Data Transferred row
    prefix=pjoin(nda_root,network,f'PHOENIX/GENERAL/{network}??/processed/{subject}/interviews/open/')


    data=1
    # if there is a valid score, data is surely here
    if score==-days_since_scan:

        if len(glob(prefix+ '*interview*_open-day*to*.csv'))<2:
            data=-days_since_scan
        
        # following could be a stricter way to detect data availability
        '''
        for desc in ['interviewRedactedTranscriptQC_open','interviewMonoAudioQC_open','interviewVideoQC_open']:

            pattern= prefix+ '*'+ desc+ f'-day*to{scan_minus_consent}.csv'
            if len(glob(pattern))!=1:
                data=-days_since_scan
                break
        '''


    # populate Protocol Followed row
    protocol=1
    if get_value(timepoint,'chrspeech_deviation')=='0' or get_value(timepoint,'chrspeech_quality')=='0':
        protocol=0


    dict2={'avl_score':score, 'avl_data':data, 'avl_protocol':protocol, 'avl_date':interview_date,
        'avl_missing':''}

    return dict2



def get_cnb_status():

    interview_date=get_value(timepoint,'chrpenn_interview_date')
    if interview_date=='':
        return {'cnb_data':'', 'cnb_protocol':'', 'cnb_date':'', 'cnb_missing':''}

    if get_value(timepoint,'chrpenn_missing')=='1':
        missing_code=get_value(timepoint,'chrpenn_missing_spec')
        return {'cnb_data':'', 'cnb_protocol':'', 'cnb_date':interview_date, 'cnb_missing':missing_code}


    scan_minus_consent=str_date_minus_str_date(consent_date,interview_date)
    days_since_scan=str_date_minus_str_date(interview_date,today)
    

    # populate Data Transferred row
    # load .UPENN.json
    # check if interview_date exists twice among all session_date
    data=-days_since_scan
    upenn=s.replace(f'.{network}.json','.UPENN.json')
    if isfile(upenn):
        with open(upenn) as f:
            dict1=json.load(f)

        count=0
        for d in dict1:
            if abs(str_date_minus_str_date(d['session_date'],interview_date))<=30:
                count+=1
        
        # NOTE some subjects may have just one session
        if count==2:
            data=1

    # populate Protocol Followed row
    protocol=1
    if get_value(timepoint,f'chrpenn_complete')!='0':
        protocol=0

    dict2={'cnb_data':data, 'cnb_protocol':protocol, 'cnb_date':interview_date,
        'cnb_missing':''}

    return dict2



if __name__=='__main__':

    nda_root='/data/predict1/data_from_nda/'
    
    parser = argparse.ArgumentParser(description='Data status generator')
    parser.add_argument('--timepoint', type=str, default='baseline', help='baseline or month_2')
    parser.add_argument('--network', type=str, required=True, help='Pronet or Prescient')

    args = parser.parse_args()

    network=args.network
    timepoint=args.timepoint

    outdir=pjoin(nda_root,f'{network}_status')

    surveys=glob(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}??/raw/*/surveys/*.{network}.json'))


    # initiate DataFrame
    df1=pd.DataFrame(columns=['day,reftime,timeofday,weekday,subject_id,site'.split(',')])

    for s in surveys:
        
        print('processing',s)

        with open(s) as f:
            dict1=json.load(f)

        consent_date=get_value('screening','chric_consent_date')

        # extract and join CHR and HC arms
        dict2=[]
        for d in dict1:
            if timepoint in d['redcap_event_name']:
                dict2.append(d)
        dict1=dict2

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
    
    
