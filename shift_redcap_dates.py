#!/usr/bin/env python

import pandas as pd
import json
import numpy as np
from os import getcwd, chdir, makedirs
from os.path import dirname, basename, abspath
from datetime import datetime, timedelta
import sys
from glob import glob
from multiprocessing import Pool
import signal


# Shift REDCap dates by one of [-14,-7,7,14] randomly chosen days
# Usage:
# __file__ NDA_ROOT "Pronet/PHOENIX/PROTECTED/*/raw/*/surveys/*.Pronet.json" /path/to/redcap_data_dict.csv
# __file__ NDA_ROOT "Pronet/PHOENIX/PROTECTED/*/raw/*/surveys/*.Pronet.json" /path/to/redcap_data_dict.csv 8
# __file__ PHOENIX_PROTECTED "*/raw/*/surveys/*.Pronet.json" /path/to/redcap_data_dict.csv 8 1
#    the trailing 1 is for force re-shift of unchanged JSONs
#    it needs to be preceded by NCPU
#    if not preceded by NCPU, 1 will be regarded as NCPU


_shift= [-14,-7,7,14]
L= len(_shift)
prob= [1/L]*L

dir_bak=getcwd()
chdir(sys.argv[1])

files=glob(sys.argv[2])

dfshift=pd.read_csv('date_offset.csv')
dfshift.set_index('subject',inplace=True)

df=pd.read_csv(sys.argv[3], encoding='ISO-8859-1')

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


def _shift_date(file):

    subject=basename(file).split('.')[0]
    
    # skip unchanged JSONs
    if sys.argv[-1]!='1' and dfshift.loc[subject,'upload']==0:
        return

    # load json
    with open(file) as f:
        dict1=json.load(f)
    
    shift= int(dfshift.loc[subject,'days'])
    
    print('Processing', file)

    for d in dict1:
        for name,value in d.items():
            try:
                df.loc[name]
            except:
                continue

            if df.loc[name,valid_header]=='date_ymd':
                if value and value not in ['-3','-9','1909-09-09','1903-03-03','1901-01-01']:
                    _format='%Y-%m-%d'
                    # shift it
                    value=datetime.strptime(value,_format)+timedelta(days=shift)
                    d[name]=value.strftime(_format)

            elif df.loc[name,valid_header]=='datetime_ymd':
                if value and value not in ['-3','-9','1909-09-09','1903-03-03','1901-01-01']:
                    _format='%Y-%m-%d %H:%M'
                    # shift it
                    value=datetime.strptime(value,_format)+timedelta(days=shift)
                    d[name]=value.strftime(_format)

    
    file=abspath(file)
    file=file.replace('PROTECTED/','GENERAL/')
    file=file.replace('/raw/','/processed/')

    makedirs(dirname(file), mode=0o775, exist_ok=True)
    with open(file,'w') as f:
        json.dump(dict1,f)



if len(sys.argv)>=5:
    ncpu=int(sys.argv[4])
else:
    ncpu=16

if ncpu==1:
    # useful for debugging
    for file in files:
        _shift_date(file)
else:
    sigint_handler= signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool= Pool(ncpu)
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        pool.map_async(_shift_date, files, error_callback=RAISE)
    except KeyboardInterrupt:
        pool.terminate()
    else:
        pool.close()
    pool.join()


chdir(dir_bak)


