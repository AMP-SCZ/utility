#!/usr/bin/env python

import pandas as pd
from redcap_config import config
import requests
import sys
import json
from tempfile import NamedTemporaryFile
from os import remove, stat
from os.path import isfile, abspath, basename, dirname, join as pjoin
from numpy import save, load
from hashlib import md5


if len(sys.argv)!=2 or sys.argv[1] in ['-h','--help']:
    print('''Usage: /path/to/import_records.py CA00007.json''')
    exit(0)


import os
dirbak= os.getcwd()
# os.chdir('/data/predict/utility/yale_nh')
dfdict= pd.read_csv('AMPSCZFormRepository_DataDictionary_2022-05-10.csv')
dfevent= pd.read_csv('AMPSCZFormRepository_InstrumentDesignations_2022-05-10.csv')
#dfdict= pd.read_csv('yale_nh_data_dict.csv')
#dfevent= pd.read_csv('yale_nh_inst_event.csv')
os.chdir(dirbak)


forms_group= dfdict.groupby('Form Name')
events_group= dfevent.groupby('unique_event_name')


with open(sys.argv[1]) as f:
    data= json.load(f)


data2= []
for visit in data:
    # data2= []
    
    redcap_event_name= visit['redcap_event_name']
    
    data1={
        'chric_record_id': data[0]['chric_record_id'],
        'redcap_event_name': redcap_event_name
    }
    
    
    for form in events_group.get_group(redcap_event_name)['form']:
        
        empty=True
        data_form={}
        for v in forms_group.get_group(form)['Variable / Field Name']:
            # try/except block for bypassing nonexistent vars in JSON
            # also for bypassing empty forms
            try:
                if visit[v]:
                    empty=False
                    data_form[v]= visit[v]
            except:
                pass
        
        # bypass empty forms
        # essential for showing blank circles in REDCap record status dashboard
        if empty:
            continue

        print(form)
        print('')

        completion= f'{form}_complete'
        data1.update(data_form)
        data1[completion]= visit[completion]
        
    
    
    data2.append(data1)


# for debugging, shift the entire following block by one tab

# save it as text and load it back to avoid REDCap import error
fw= NamedTemporaryFile('w', delete=False)
json.dump(data2,fw)
fw.close()

with open(fw.name) as f:
    data2= f.read()    

remove(fw.name)


fields = {
    'token': config['api_token'],
    'content': 'record',
    'action': 'import',
    'format': 'json',
    'type': 'flat',
    'data': data2,
    'overwriteBehavior': 'overwrite',
    'returnContent': 'count',
    'returnFormat': 'json'
}

r = requests.post(config['api_url'], data= fields)    
print('HTTP Status: ' + str(r.status_code))
print(r.json())

# break 

