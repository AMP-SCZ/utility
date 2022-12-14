#!/usr/bin/env python

from shutil import copyfile
from yaml import safe_load
from glob import glob
from datetime import date
from os import getcwd, chdir, environ
from os.path import isfile
import sys
import re

suffix=date.today().strftime('%d.%m.%Y.csv')

with open('rename_RPMS_vars.yaml') as f:
    dict1=safe_load(f)

dir_bak=getcwd()
chdir(sys.argv[1])
    
for pattern in dict1.keys():

    if environ['HOSTNAME'].endswith('orygen.org.au'):
        # rename vars at RPMS end
        file=pattern+suffix
        if not isfile:
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

    
    with open(file) as f:
        content=f.read()
        header=content.split('\n')[0]
        
    
    for line in dict1[pattern]:
        v,vnew=line.split(',')
        
        if vnew not in header:
            content=content.replace(v,vnew)
        

    copyfile(file, file+'.bak')
    with open(file,'w') as f:
        f.write(content)

chdir(dir_bak)

