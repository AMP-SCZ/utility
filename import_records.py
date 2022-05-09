#!/usr/bin/env python

from redcap_config import config
import requests
import sys
import json
from copy import deepcopy
from tempfile import NamedTemporaryFile
from os import remove, stat
from os.path import isfile, abspath, basename, dirname, join as pjoin
from numpy import save, load
from hashlib import md5


if len(sys.argv)!=2 or sys.argv[1] in ['-h','--help']:
    print('''Usage: /path/to/import_records.py CA00007.json''')
    exit(0)

with open(sys.argv[1]) as f:
    surv= json.load(f)


# delete all vars that end with _complete
surv1= deepcopy(surv)
for i in range(len(surv1)):
    for key,value in surv[0].items():
        if key.endswith('_complete'):
            del surv1[i][key]


# save it as text and load it back to avoid REDCap import error
fw= NamedTemporaryFile('w', delete=False)
json.dump(surv1,fw)
fw.close()

with open(fw.name) as f:
    data= f.read()    

remove(fw.name)


fields = {
    'token': config['api_token'],
    'content': 'record',
    'action': 'import',
    'format': 'json',
    'type': 'flat',
    'data': data,
    'overwriteBehavior': 'overwrite',
    'returnContent': 'count',
    'returnFormat': 'json'
}


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
    
    print(json_file, 'does not exist in REDCap or has been modified, uploading to REDCap')
    
    # upload to REDCap
    r = requests.post(config['api_url'], data=fields)
    print('HTTP Status: ' + str(r.status_code))
    print(r.json())
    
    # save new hash
    save(hashfile, hashes1)

else:
    print(json_file, 'has not been modified, skipping')
