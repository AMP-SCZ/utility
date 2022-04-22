#!/usr/bin/env python

from redcap_config import config
import requests
import sys
import json
from copy import deepcopy
from tempfile import NamedTemporaryFile
from os import remove


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

r = requests.post(config['api_url'], data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.json())


