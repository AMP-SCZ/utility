#!/usr/bin/env python

from shutil import move
from yaml import safe_load
from glob import glob
from datetime import date, datetime
from os import getcwd, chdir, environ
from os.path import isfile, dirname, basename
import sys
import pandas as pd

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
    {__file__} /mnt/prescient/RPMS_incoming/
    {__file__} /mnt/prescient/RPMS_incoming/ 31.12.2022.csv
    {__file__} /mnt/prescient/RPMS_incoming/ 31.12.2022.csv /path/to/replace_RPMS_values.yaml
First arg is mandatory, rest are optional.''')
    exit(0)

try:
    suffix=sys.argv[2]
except:
    suffix=date.today().strftime('%d.%m.%Y.csv')

try:
    yaml_file=sys.argv[3]
except:
    yaml_file=dirname(__file__)+'/replace_RPMS_values.yaml'

with open(yaml_file) as f:
    dict1=safe_load(f)

dir_bak=getcwd()
chdir(sys.argv[1])
    
for pattern in dict1.keys():

    if environ['HOSTNAME'].endswith('orygen.org.au'):
        # rename vars at RPMS end
        file=pattern+suffix
        if not isfile(file):
            # this file exists at DPACC
            # skip DPACC suffixes
            continue

    else:
        # rename vars at DPACC end
        file=glob('*'+pattern)
        if not file:
            # this file does not exist for this subject
            # skip RPMS prefixes
            continue

        file=file[0]

    
    print('Processing',file)
    data=pd.read_csv(file,dtype=str,keep_default_na=False)
    datanew=data.copy()
    replaced=False
    
    for line in dict1[pattern]:
        v,rpms,redcap=line.split(',')

        _rpms=rpms.split()
        _redcap=redcap.split()
        dict2=dict(zip(_rpms,_redcap))
        
        
        for i,row in data.iterrows():
            if pd.isna(row[v]):
                continue

            if row[v] in _rpms:
                datanew.loc[i,v]=dict2[row[v]]
                replaced=True


    if replaced:
        datanew.to_csv(file,index=False)

chdir(dir_bak)

