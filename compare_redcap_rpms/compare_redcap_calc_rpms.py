#!/usr/bin/env python

import pandas as pd
import json
import numpy as np
from os import getcwd, chdir
from os.path import dirname
import sys


# Compare REDCap computed calc fields against those extracted from RPMS
# Usage:
# __file__ /path/to/redcap_rpms_extracts.csv


dir_bak=getcwd()

df=pd.read_csv(sys.argv[1])
chdir(dirname(sys.argv[1]))
groups=df.groupby('subject')

for sub in ['ME21922','ME22598','ME78581']:

    dfsub=groups.get_group(sub).set_index('variable')

    dfsub1=pd.DataFrame(columns=['variable','type','rpms_value','redcap_value'])


    # load json
    with open(f'{sub}.json') as f:
        dict1=json.load(f)

    
    i=0
    for v in dfsub.index:
               
        if 'chrscid_' in v:
            event='baseline_arm_1'
        else:
            event='screening_arm_1'       
               
        for d in dict1:
        
            # go to event
            if d['redcap_event_name']==event:
                
                try:
                    # dfsub.at[v,'redcap_value']=d[v]
                    if pd.isna(dfsub.loc[v,'value']) and d[v]=='':
                        continue
                        
                    elif dfsub.loc[v,'value']!=d[v]:
                        
                        dfsub1.loc[i]= [v,dfsub.loc[v,'type'],dfsub.loc[v,'value'],d[v]]
                        i+=1
                        
                except KeyError:
                    # print(v)
                    pass
                
            
    # dfsub.reset_index().to_csv(f'{sub}.csv', index=False)
    dfsub1.to_csv(f'{sub}.csv', index=False)
    
chdir(dir_bak)


