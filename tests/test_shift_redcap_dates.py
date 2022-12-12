#!/usr/bin/env python

import pandas as pd
import json
import numpy as np
from os import getcwd, chdir, makedirs
from os.path import dirname, abspath, basename
from datetime import datetime, timedelta
import sys
from glob import glob
from multiprocessing import Pool
import signal

# Shift REDCap dates by one of [-14,-7,7,14] randomly chosen days
# Usage:
# __file__ NDA_ROOT /path/to/redcap_data_dict.csv "Pronet/PHOENIX/PROTECTED/*/raw/*/surveys/*.Pronet.json"

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


def RAISE(err):
    raise err

def _test_shift(file):
    # load original json
    with open(file) as f:
        dict1=json.load(f)
    
    # load shifted json
    file=abspath(file)
    file=file.replace('PROTECTED/','GENERAL/')
    file=file.replace('/raw/','/processed/')
    with open(file) as f:
        dict2=json.load(f)
        
    print('Comparing', file)
    
    _shift={}
    for d1,d2 in zip(dict1,dict2):
        for name,value in d1.items():
            try:
                df.loc[name]
            except:
                continue

            if df.loc[name,valid_header]=='date_ymd':
                _format='%Y-%m-%d'
                if value and value not in ['-3','-9','1909-09-09','1903-03-03','1901-01-01']:
                    _shift[datetime.strptime(d2[name],_format) - datetime.strptime(d1[name],_format)]=''
            elif df.loc[name,valid_header]=='datetime_ymd':
                _format='%Y-%m-%d %H:%M'
                if value and value not in ['-3','-9','1909-09-09','1903-03-03','1901-01-01']:
                    _shift[datetime.strptime(d2[name],_format) - datetime.strptime(d1[name],_format)]=''
        

    # print(_shift.keys(),'\n')

    return list(_shift.keys())


if len(sys.argv)==5:
    ncpu=int(sys.argv[4])
else:
    ncpu=16

if ncpu==1:
    # useful for debugging
    for file in files:
        _test_shift(file)
else:
    sigint_handler= signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool= Pool(ncpu)
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        res=pool.map_async(_test_shift, files, error_callback=RAISE)
        shifts= res.get()
    except KeyboardInterrupt:
        pool.terminate()
    else:
        pool.close()
    pool.join()


for f,s in zip(files,shifts):
    print(basename(f).split('.')[0],s)

chdir(dir_bak)


