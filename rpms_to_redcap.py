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


def _visit_to_event(chr_hc, form, visit_num):
    pass
    
    prefix= rpmsTime_to_redcapTime[visit_num]
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
    print('''Usage:
    /path/to/import_records.py ME57953.csv forms-dir API_TOKEN 1
    /path/to/import_records.py ME57953/surveys/ forms-dir API_TOKEN 1
first input can be either file or directory
forms-dir is the directory with *_DataDictionary_*.csv and *_InstrumentDesignations_*.csv files
1 is for force re-upload''')
    exit(0)


if sys.argv[-1]=='1':
    pass
else:
    # load and compare old os.stat() of REDCap JSON file
    hashfile= pjoin(abspath(dirname(__file__)), '.json_os.stat_hashes.npy')
    if isfile(hashfile):
        hashes= load(hashfile, allow_pickle=True).item()
    else:
        hashes= {}

    json_file= basename(sys.argv[1])
    if json_file in hashes:
        old_hash= hashes[json_file]
    else:
        old_hash= ''

    curr_stat= stat(sys.argv[1])
    curr_stat= '_'.join(str(s) for s in [curr_stat.st_uid,curr_stat.st_size,curr_stat.st_mtime])
    curr_hash= md5(curr_stat.encode('utf-8')).hexdigest()

    hashes1= deepcopy(hashes)
    hashes1[json_file]= curr_hash
    if curr_hash != old_hash:
        print(json_file, 'does not exist in REDCap or has been modified, preparing for upload to REDCap')
    else:
        print(json_file, 'has not been modified, skipping')
        exit()


dirbak= getcwd()
chdir(sys.argv[2])
dfdict= pd.read_csv(glob('*_DataDictionary_*')[0])
dfevent= pd.read_csv(glob('*_InstrumentDesignations_*')[0])
_dfevent= dfevent.set_index(['arm_num', 'form']).sort_index()
chdir(dirbak)


forms_group= dfdict.groupby('Form Name')
events_group= dfevent.groupby('unique_event_name')


subjectkey= sys.argv[1].split('_')[0]
incl_excl= subjectkey+ '_inclusionexclusion_criteria_review.csv'
if not isfile(incl_excl):
    raise FileNotFoundError(f'Cannot determine redcap_event_name w/o {incl_excl} file')


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
    elif status==2:
        return 2


df= pd.read_csv(incl_excl)
try:
    chr_hc= int(df['chrcrit_part'])
except ValueError:
    raise ValueError(f'Value of chrcrit_part in {incl_excl} must be 1(CHR) or 2(HC)')

form= re.search(f'{subjectkey}_(.+?).csv', sys.argv[1]).group(1)

data= pd.read_csv(sys.argv[1])

data2= []
for _,visit in data.iterrows():
    
    # skip Parent/Guardian consent if any
    if 'version' in visit and visit['version']=='Parent/Guardian':
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
        # try/except block for bypassing nonexistent vars in JSON
        # also for bypassing empty forms
        try:
            # consider non-empty only
            if pd.isna(visit[v]):
                continue
            elif isinstance(visit[v],str) and visit[v].lower() in ['','-','none','not applicable', 'n/a','na']:
                continue
            elif visit[v] in [-3,-99]:
                continue
                
            # leave checkbox variables out of consideration
            # to decide whether a form is empty
            if '___' not in v:
                empty=False

            # number
            try:
                residue= int(visit[v])-float(visit[v])
                if residue:
                    # float
                    value= visit[v]
                else:
                    # int
                    value= int(visit[v])

                    # RPMS yields 0 for unchecked-single-choice radio variables
                    # but REDCap only accepts '' for such
                    # e.g. _missing variables
                    # REDCap coded as 1 or '', RPMS coded as 1 or 0
                    if value==0 and row['Field Type']=='radio' and \
                        len(row['Choices, Calculations, OR Slider Labels'].split('|'))==1:
                        value=''
                        
                value= str(value)

            # date, string
            except ValueError:
                dtype= row['Text Validation Type OR Show Slider Number']
                if dtype=='date_ymd' or dtype=='datetime_ymd':

                    # date_ymd
                    if len(visit[v])==10:
                        try:
                            # interview_date e.g. 11/30/2022
                            value= datetime.strptime(visit[v], '%m/%d/%Y').strftime('%Y-%m-%d')
                        except ValueError:
                                # psychs form e.g. 03/03/1903
                                value= datetime.strptime(visit[v], '%d/%m/%Y').strftime('%Y-%m-%d')

                    # datetime_ymd
                    elif len(visit[v])>10:
                        value= datetime.strptime(visit[v], '%d/%m/%Y %I:%M:%S %p').strftime('%Y-%m-%d')
                        
                elif dtype=='time':
                    value= visit[v][:5]
                else:
                    # string
                    value= visit[v]

            data_form[v]= value

        except KeyError:
            pass
    

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
    # print(data2)
    # print('')
    

# for debugging, shift the entire following block by one tab

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
    'overwriteBehavior': 'normal',
    'returnContent': 'count',
    'returnFormat': 'json'
}

r = requests.post('https://redcap.partners.org/redcap/api/', data= fields)
print('\t','HTTP Status: ' + str(r.status_code))
print('\t',r.json())

# break 

if sys.argv[-1]=='1':
    pass
else:
    # save new hash
    save(hashfile, hashes1)



