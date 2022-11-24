#!/usr/bin/env python

import pandas as pd
import json
import numpy as np
from os import getcwd, chdir
from datetime import date, timedelta

# Shift REDCap dates by one of [-14,-7,7,14] randomly chosen days
# Usage:
# __file__ NDA_ROOT /path/to/redcap_data_dict.csv "Pronet/PHOENIX/PROTECTED/*/raw/*/surveys/*.Pronet.json"

_shift= [-14,-7,7,14]
L= len(_shift)
prob= [1/L]*L

dir_bak=getcwd()
chdir(sys.argv[1])
files=glob(sys.argv[2])

df=pd.read_csv(sys.argv[3], encoding='ISO-8859-1')

# when downloaded through GUI
var_header='Variable / Field Name'
field_type='Field Type'
form_header='Form Name'
branch_header='Branching Logic (Show field only if...)'
calc_header='Choices, Calculations, OR Slider Labels'

# when downloaded through API
if var_header not in df:
    var_header='field_name'
    field_type='field_type'
    form_header='form_name'
    branch_header='branching_logic'
    calc_header='select_choices_or_calculations'

df.set_index(var_header,inplace=True)


for file in files[:1]:
    # load json
    with open(file) as f:
        dict1=json.load(f)
        
    # randomize according to multinomial distribution
    shift= values[np.where(np.random.multinomial(1,prob))[0][0]]    
    
    # TBD find and load metadata
    metadata.at[subject,days_shift]=shift
        
    for d in dict1:
        for name,value in d.items():
            if df.loc[name,field_type]=='date_ymd':
                if not (pd.isna(value) and np.isnan(value) and value=='')
                    # shift it
                    d[name]=value+timedelta(days=shift)


file=file.replace('PROTECTED/','GENERAL/')
file=file.replace('/raw/','/processed/')                    
with open(file,'w') as f:
    json.dump(dict1)    


# save metadata

# skip unchanged JSONs

chdir(dir_bak)


