#!/usr/bin/env python
import json, sys

with open(sys.argv[1]) as f:
    dict1= json.load(f)

dict2={}
dict2['config']=dict1['config']['0']
dict2['name']=dict1['name']+'_copy'

with open(sys.argv[2], 'w') as f:
    json.dump(dict2,f,indent=3)
