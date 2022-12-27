#!/usr/bin/env python

from shutil import move
from yaml import safe_load
from glob import glob
from datetime import date
from os import getcwd, chdir, environ
from os.path import isfile, dirname, basename
import sys
import pandas as pd


suffix=date.today().strftime('%d.%m.%Y.csv')
suffix='26.12.2022.csv'

with open(dirname(__file__)+'/replace_RPMS_values.yaml') as f:
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

    df=pd.read_csv(file)
    
    
    for line in dict1[pattern]:
        v,rpms,redcap=line.split(',')
        dict2=dict(zip(rpms.split(),redcap.split()))

        for i in df.index:
            try:
                df.at[i,v]=dict2[str(int(df.loc[i,v]))]
            except:
                pass

        # print('')

    # move(file, file+'.bak')
    df.to_csv(f'~/tmp/{basename(file)}', index=False)

chdir(dir_bak)

