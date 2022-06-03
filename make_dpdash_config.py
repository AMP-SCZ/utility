#!/usr/bin/env python

from copy import deepcopy
import json
import sys

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {__file__} /path/to/AMPSCZ-SITE-assessment-day1to9999.csv
Define one item in https://predict.bwh.harvard.edu/dpdash/u/configure web interface, 
download that config, update it with all items from -day1to1.csv files''')
    exit(0)

in_json= sys.argv[1]
with open(in_json) as f:
    dict1= json.load(f)

cols=sys.argv[2:]
template= dict1['config'][0]
dict1['config']=[]
for col in cols:
    template2= deepcopy(template)
    template2['variable']= col
    template2['label']=col
    dict1['config'].append(template2)

dict1['name']=dict1['name']+'-2'

with open(in_json.split('.json')[0]+'-2.json','w') as f:
    json.dump(dict1,f,indent=3)
    
