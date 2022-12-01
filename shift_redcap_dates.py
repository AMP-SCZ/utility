#!/usr/bin/env python

import pandas as pd
import json
import numpy as np
from os import getcwd, chdir, makedirs
from os.path import dirname
from datetime import datetime, timedelta
import sys
from glob import glob


# Shift REDCap dates by one of [-14,-7,7,14] randomly chosen days
# Usage:
# __file__ NDA_ROOT /path/to/redcap_data_dict.csv "Pronet/PHOENIX/PROTECTED/*/raw/*/surveys/*.Pronet.json"

_shift= [-14,-7,7,14]
L= len(_shift)
prob= [1/L]*L

dir_bak=getcwd()
chdir(sys.argv[1])

df=pd.read_csv(sys.argv[2], encoding='ISO-8859-1')

files=glob(sys.argv[3])


# when downloaded through GUI
var_header='Variable / Field Name'
field_type='Field Type'
form_header='Form Name'
branch_header='Branching Logic (Show field only if...)'
calc_header='Choices, Calculations, OR Slider Labels'
valid_header='Text Validation Type OR Show Slider Number'

# when downloaded through API
if var_header not in df:
    var_header='field_name'
    field_type='field_type'
    form_header='form_name'
    branch_header='branching_logic'
    calc_header='select_choices_or_calculations'
    valid_header='text_validation_type_or_show_slider_number'

df.set_index(var_header,inplace=True)


for file in files[:2]:
    # load json
    with open(file) as f:
        dict1=json.load(f)
        
    # randomize according to multinomial distribution
    shift= _shift[np.where(np.random.multinomial(1,prob))[0][0]]
    
    # TBD find and load metadata
    # metadata.at[subject,days_shift]=shift
        
    print('Processing', file)

    for d in dict1:
        for name,value in d.items():
            try:
                df.loc[name]
            except:
                continue

            if df.loc[name,valid_header]=='date_ymd':
                if value:
                    # shift it
                    value=datetime.strptime(value,'%Y-%m-%d')+timedelta(days=shift)
                    d[name]=value.strftime('%Y-%m-%d')


    file=file.replace('PROTECTED/','GENERAL/')
    file=file.replace('/raw/','/processed/')

    makedirs(dirname(file), mode=0o775, exist_ok=True)
    with open(file,'w') as f:
        json.dump(dict1,f)


# save metadata

# skip unchanged JSONs

chdir(dir_bak)


