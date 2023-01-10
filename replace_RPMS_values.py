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
    with open(file) as f:
        content=f.read()
    
    data=content.split('\n')
    header=data[0].split(',')
    
    for line in dict1[pattern]:
        v,rpms,redcap=line.split(',')
        dict2=dict(zip(rpms.split(),redcap.split()))
        
        # find the position of the variable in header
        absent=1
        for ind,h in enumerate(header):
            if h==v:
                absent=0
                break
        
        if absent:
            continue

        for i,row in enumerate(data):
            
            # skip header
            if i==0:
                continue


            # for value replacement, consider only subject lines
            # they start as e.g. 20/01/2023 2:10:00 AM,ME12345,01/20/2023
            # all other lines are due to \n within a cell
            _row=row.split(',')

            try:
                # LastModifiedDate
                datetime.strptime(_row[0], '%d/%m/%Y %I:%M:%S %p')
                # subjectkey
                assert len(_row[1])==7
                # *_interview_date
                datetime.strptime(_row[2], '%m/%d/%Y')
            except:
                continue

            # NOTE the above line detection scheme will not be able to replace
            # values positioned after cells with \n
            
            
            # replace the value in corresponding position
            # try-except for skipping '' and missing data codes
            # replaced for skipping subjects with no value for v
            replaced=0
            try:
                _row[ind]=dict2[_row[ind]]
                replaced=1
            except:
                pass
            
            if replaced:
                data[i]=','.join(_row)
            
    datanew='\n'.join(data)

    move(file, file+'.bak')
    with open(file,'w') as f:
        f.write(datanew)

chdir(dir_bak)

