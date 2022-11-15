#!/usr/bin/env python

import os
os.environ['OPENBLAS_NUM_THREADS']='16'

import sys
from os.path import isfile, abspath, dirname, join as pjoin
from os import getcwd, chdir
import pandas as pd
from datetime import datetime
from glob import glob

# ground truth dictionary
df1=pd.read_csv(sys.argv[1], encoding='ISO-8859-1')

# when downloaded through GUI
var_header='Variable / Field Name'
form_header='Form Name'
branch_header='Branching Logic (Show field only if...)'
calc_header='Choices, Calculations, OR Slider Labels'

# when downloaded through API
if var_header not in df1:
    var_header='field_name'
    form_header='form_name'
    branch_header='branching_logic'
    calc_header='select_choices_or_calculations'

ground_groups=df1.groupby(form_header)


dir_bak= getcwd()
chdir('/data/predict/data_from_nda/Prescient/PHOENIX/PROTECTED/')

dfall={}
for form in ground_groups.groups.keys():
       
    if '_consent_' in form and 'informed_consent_run_sheet' not in form:
        continue
    
    # print(form)
    
    files=glob(f'Prescient??/raw/*/surveys/*_{form}.csv')
    
    dfform={}
    for file in files:
        flat= file+'.flat'
        
        if isfile(flat):
            file= flat
        
        try: 
            df=pd.read_csv(file, encoding='ISO-8859-1', on_bad_lines='skip', engine='python')
        except pd.errors.EmptyDataError:
            continue
        
        for e in df.columns[6:]:
            dfform[e]=''
            
        
    # print(len(dfform))
    dfall.update(dfform)
    

chdir(dir_bak)

print(len(dfall))


# construct dict from AMP-SCZ variables for O(1) look up
dict_ampscz={}
for v in df1[var_header].values:
    dict_ampscz[v]=''

# perform O(1) lookup for RPMS variables
for var in dfall.keys():
    # if '___' in var:
    #     continue

    try:
        dict_ampscz[var]
    except KeyError:
        print(var)

