#!/usr/bin/env python

import pandas as pd

import socket
from urllib3.connection import HTTPConnection

HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 60),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
        (socket.SOL_TCP, socket.TCP_KEEPCNT, 6)
    ]
)

import requests
import sys
import json
from copy import deepcopy
from tempfile import NamedTemporaryFile
from os import remove, stat, getcwd, chdir, stat
from os.path import isfile, abspath, basename, dirname, join as pjoin
from numpy import save, load
from hashlib import md5
from glob import glob
import re
import numpy as np
from datetime import datetime
from time import sleep
from util import get_consent

rpmsTime_to_redcapTime= {
    1: 'screening',
    2: 'baseline',
    3: 'month_1',
    4: 'month_2',
    5: 'month_3',
    6: 'month_4',
    7: 'month_5',
    8: 'month_6',
    9: 'month_7',
    10: 'month_8',
    11: 'month_9',
    12: 'month_10',
    13: 'month_11',
    14: 'month_12',
    15: 'month_18',
    16: 'month_24',
    98: 'conversion',
    99: 'floating'
}


def _date(time_value):
    
    if len(time_value)==10:
    
        try:
            # interview_date e.g. 11/30/2022
            int_value= datetime.strptime(time_value, '%m/%d/%Y')
        except ValueError:
            # psychs form e.g. 03/03/1903
            int_value= datetime.strptime(time_value, '%d/%m/%Y')

    elif len(time_value)>10:
        # all other forms e.g. 1/05/2022 12:00:00 AM
        int_value= datetime.strptime(time_value, '%d/%m/%Y %I:%M:%S %p')
        
    return int_value


def _visit_to_event(chr_hc, form, visit_num):
    
    try:
        visit_num=int(visit_num)
    except ValueError:
        visit_num=int(float(visit_num))
            
    prefix= rpmsTime_to_redcapTime[int(visit_num)]
    events= _dfevent.loc[(chr_hc, form)]['unique_event_name'].values
    for e in events:
        if prefix in e:
           redcap_event_name= e
           break
           
    try:
        return redcap_event_name
    except UnboundLocalError:
        raise UnboundLocalError(f'{chr_hc}, {form}, {visit_num}')


if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
    {abspath(__file__)} ME57953.csv forms-dir API_TOKEN 1
execute it within /path/to/ME57953/surveys/ directory
forms-dir is the directory with *_DataDictionary_*.csv and *_InstrumentDesignations_*.csv files
optional: 1 is for force re-upload''')
    exit(0)


subjectkey= sys.argv[1].split('_')[0]

if sys.argv[-1]=='1':
    pass
else:
    subject=basename(sys.argv[1]).split('_')[0]
    
    hashfile=subjectkey+'_hashes.csv'
    if isfile(hashfile):

        dfshift=pd.read_csv(hashfile)
        dfshift.set_index('form',inplace=True)

        # skip unchanged CSVs
        if sys.argv[1] in dfshift.index and dfshift.loc[sys.argv[1],'upload']==0:
            print(sys.argv[1], 'has not been modified, skipping')
            exit()
        # if a form is not in dfshift.index, that got downloaded after {subjectkey}_hashes.csv was created
        # that is a new one and we let it upload
    
    else:
        print('Could not find {}, so force uploading {}'.format(hashfile,sys.argv[1]))



dirbak= getcwd()
chdir(sys.argv[2])
dfdict= pd.read_csv(glob('*_DataDictionary_*')[0])
dfevent= pd.read_csv(glob('*_InstrumentDesignations_*')[0])
_dfevent= dfevent.set_index(['arm_num', 'form']).sort_index()
chdir(dirbak)


forms_group= dfdict.groupby('Form Name')
events_group= dfevent.groupby('unique_event_name')


incl_excl= subjectkey+ '_inclusionexclusion_criteria_review.csv'
inform_consent= subjectkey+ '_informed_consent_run_sheet.csv'
if not isfile(inform_consent):
    raise FileNotFoundError(f'Cannot determine redcap_event_name w/o {inform_consent} file')


# load files for populating {form}_completion variable
entry_status_df= pd.read_csv(subjectkey+ '_entry_status.csv')
entry_status_df.set_index(['InstrumentName', 'visit'],inplace=True)
redcap_rpms_labels_df= pd.read_csv(pjoin(abspath(dirname(__file__)),'rpms_form_labels.csv'))
redcap_rpms_labels_df.set_index('redcap',inplace=True)

def entry_status(redcap_label,rpms_visit):
    try:
        rpms_label= redcap_rpms_labels_df.loc[redcap_label,'rpms']
        status= entry_status_df.loc[(rpms_label,rpms_visit),'CompletionStatus']
    except KeyError:
        return ''

    '''
    RPMS policy
    status color  meaning
    0      Red    No data entered
    1      Orange Data partially entered
    2      Green  All data entered
    '''

    status=int(status)
    if status==0:
        return ''
    elif status==1:
        return 0
    elif status>=2 and status<=4:
        return 2



# one try-except block to handle absence of incl_excl and empty chrcrit_part
try:
    df= pd.read_csv(incl_excl)
    chr_hc= int(df['chrcrit_part'])
    
except (FileNotFoundError,ValueError):
    
    _,chr_hc=get_consent(inform_consent)
    
    if chr_hc=='UHR':
        chr_hc=1
    elif chr_hc=='HealthyControl':
        chr_hc=2
    else:
        raise ValueError(f'CHR/HC status could not be determined')

form= re.search(f'{subjectkey}_(.+?).csv', sys.argv[1]).group(1)

if chr_hc==1:
    if sys.argv[1].endswith('_psychs_p1p8_fu_hc.csv') or sys.argv[1].endswith('_psychs_p9ac32_fu_hc.csv'):
        exit(0)
        
elif chr_hc==2:
    if sys.argv[1].endswith('_psychs_p1p8_fu.csv') or sys.argv[1].endswith('_psychs_p9ac32_fu.csv'):
        exit(0)

data= pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)


for _,visit in data.iterrows():
    data2= []
    
    # skip Parent/Guardian consent if YP consent is present
    if 'version' in visit and visit['version']=='Parent/Guardian' and 'YP' in data['version'].unique():
        continue
    
    redcap_event_name= _visit_to_event(chr_hc, form, visit['visit'])
    
    data1={
        'chric_record_id': visit['subjectkey'],
        'redcap_event_name': redcap_event_name
    }
    
    
    print(redcap_event_name)

    empty=True
    data_form={}
    for _,row in forms_group.get_group(form).iterrows():
        v= row['Variable / Field Name']
        dtype= row['Text Validation Type OR Show Slider Number']
        ftype= row['Field Type']
        try:
            annotation= row['Field Annotation'].strip()
        except AttributeError:
            annotation= ''

        # try/except block for bypassing nonexistent vars in CSV
        # also for bypassing empty forms
        try:
            # consider non-empty only
            if visit[v]=='':
                continue
                
            elif visit[v].lower() in ['-','none','not applicable', 'n/a','na']:
                if ftype=='calc':
                    # always reject not applicable
                    continue
                elif ftype=='text' and not pd.isna(dtype):
                    # if any validation is set, reject not applicable
                    continue

            elif visit[v] in ['-3','-9','1903-03-03','1909-09-09'] and annotation=='@NOMISSING':
                continue
            elif visit[v] in ['-3','-9','-99'] and ftype in ['dropdown','yesno','radio','checkbox']:
                # these codes do not fit these field types
                continue
                
            # leave checkbox variables out of consideration
            # to decide whether a form is empty
            if '___' not in v:
                empty=False

            # number
            try:
                _value=visit[v]
                if _value=='True':
                    _value=1
                elif _value=='False':
                    _value=0

                _value=float(_value)
                residue= int(_value)-_value
                if residue:
                    # float
                    value= _value
                    if dtype=='integer':
                        value=round(_value)

                else:
                    # int
                    value= int(_value)

                    # RPMS yields 0 for unchecked-single-choice radio variables
                    # but REDCap only accepts '' for such
                    # e.g. _missing variables
                    # REDCap coded as 1 or '', RPMS coded as 1 or 0
                    if value==0 and ftype=='radio' and \
                        len(row['Choices, Calculations, OR Slider Labels'].split('|'))==1:
                        value=''
                        
                value= str(value)

            # date, string
            except ValueError:

                if dtype=='date_ymd':
                    _string=_date(visit[v])
                    value=_string.strftime('%Y-%m-%d')

                elif dtype=='datetime_ymd':
                    _string=_date(visit[v])
                    value=_string.strftime('%Y-%m-%d %H:%M')
                    
                elif dtype=='time':
                    value= visit[v][:5]
                else:
                    # string
                    value= visit[v]

            data_form[v]= value

        except KeyError:
            pass
    
    
    if form=='informed_consent_run_sheet':
        if data['interview_date'].unique().shape[0]>1:
            consent_sorted,_=get_consent(data)
            orig_consent=consent_sorted.iloc[0]['interview_date']
            data_form['chric_consent_date']= _date(orig_consent).strftime('%Y-%m-%d')
    
    
    if form=='sociodemographics':
        if chr_hc==1:
            data_form['chrdemo_age_mos_chr'] = visit['interview_age']
        elif chr_hc==2:
            data_form['chrdemo_age_mos_hc'] = visit['interview_age']


    if form=='inclusionexclusion_criteria_review':
        if pd.isna(visit['chrcrit_part']):
            data_form['chrcrit_part']=chr_hc

    completion= f'{form}_complete'
    # bypass empty forms
    # essential for showing blank circles in REDCap record status dashboard
    if empty:
        continue

    '''
    REDCap policy
    value  color  meaning
    ''     Blank  Incomplete (no data saved)
    0      Red    Incomplete
    1      Yellow Unverified
    2      Green  Complete
    '''

    print('\t',form)

    data1.update(data_form)
    data1[completion]= entry_status(form,visit['visit'])

    data2.append(data1)
    # print('\t',data2)
    


    # save it as text and load it back to avoid REDCap import error
    fw= NamedTemporaryFile('w', delete=False)
    json.dump(data2,fw)
    fw.close()

    with open(fw.name) as f:
        data2= f.read()

    remove(fw.name)


    fields = {
        'token': sys.argv[3],
        'content': 'record',
        'action': 'import',
        'format': 'json',
        'type': 'flat',
        'data': data2,
        'overwriteBehavior': 'overwrite',
        'returnContent': 'count',
        'returnFormat': 'json'
    }

    try:
        r = requests.post('https://redcap.partners.org/redcap/api/', data= fields)
    except requests.exceptions.ConnectionError:
        # wait 180 seconds before retrying
        sleep(180)
        r = requests.post('https://redcap.partners.org/redcap/api/', data= fields)

    print('\t','HTTP Status: ' + str(r.status_code))
    print('\t',r.json())

    print('')
