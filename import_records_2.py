#!/usr/bin/env python

import pandas as pd
import json
from tempfile import NamedTemporaryFile
from os import remove
import requests
from redcap_config import config

dfdict= pd.read_csv('AMPSCZFormRepository_DataDictionary_2022-05-10.csv')
forms_group= dfdict.groupby('Form Name')

dfevent= pd.read_csv('AMPSCZFormRepository_InstrumentDesignations_2022-05-10.csv')
events_group= dfevent.groupby('unique_event_name')


with open('/data/predict/data_from_nda/Pronet/PHOENIX/PROTECTED/PronetYA/raw/YA00037/surveys/YA00037.Pronet.json') as f:
    data= json.load(f)


data2= []
for visit in data:
    # data2= []
    
    redcap_event_name= visit['redcap_event_name']
    
    data1={
        'chric_record_id': data[0]['chric_record_id'],
        'redcap_event_name': redcap_event_name
    }
    
    
    vars=[]
    for form in events_group.get_group(redcap_event_name)['form']:
        for v in forms_group.get_group(form)['Variable / Field Name']:
            vars.append(v)
        print(form)
        print('')

        completion= f'{form}_complete'
        data1[completion]= visit[completion]
        
    
    # join the following for to above
    for key in vars:
        try:
            data1[key]= visit[key]
        except:
            pass
            # print(f'form: {form}, var: {key}')
    
    
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

