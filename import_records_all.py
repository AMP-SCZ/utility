#!/usr/bin/env python

import pandas as pd
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


if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print('''Usage: /path/to/import_records.py CA00007.json forms-dir API_TOKEN 1
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
chdir(dirbak)


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
    
    
    print(redcap_event_name)

    for form in events_group.get_group(redcap_event_name)['form']:

        empty=True
        data_form={}
        for v in forms_group.get_group(form)['Variable / Field Name']:
            # try/except block for bypassing nonexistent vars in JSON
            # also for bypassing empty forms
            try:
                if visit[v]:
                    # leave checkbox variables out of consideration
                    # to decide whether a form is empty
                    if '___' not in v:
                        empty=False
                    data_form[v]= visit[v]
            except:
                pass
        
        
        completion= f'{form}_complete'
        # bypass empty forms
        # essential for showing blank circles in REDCap record status dashboard
        if empty:
            continue
        # calculated fields may still pose a form as non-empty
        # see how REDCap circles are colored
        # https://user-images.githubusercontent.com/35086881/168111407-d99c0a49-d33c-4cd9-9530-79f0debd9690.png
        


        print('\t',form)

        data1.update(data_form)
        data1[completion]= visit[completion]
        
        
    data2.append(data1)

    print('')
    

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
print('HTTP Status: ' + str(r.status_code))
print(r.json())

# break 

if sys.argv[-1]=='1':
    pass
else:
    # save new hash
    save(hashfile, hashes1)


