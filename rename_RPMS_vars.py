#!/usr/bin/env python

from shutil import copyfile
from yaml import safe_load
from glob import glob
from datetime import date
from os import getcwd, chdir, environ
import sys
import re

if environ['HOSTNAME'].endswith('orygen.org.au'):
    suffix=date.today().strftime('%d.%m.%Y.csv')

with open('rename_RPMS_vars.yaml') as f:
    dict1=safe_load(f)

dir_bak=getcwd()
chdir(sys.argv[1])
    
for pattern in dict1.keys():

    if environ['HOSTNAME'].endswith('orygen.org.au'):
        file=pattern+suffix
    else:
        try:
            file=glob('*'+pattern)[0]
        except IndexError:
            # file does not exist
            continue

    
    with open(file) as f:
        content=f.read()
        header=content.split('\n')[0]
        
    
    for line in dict1[prefix]:
        v,vnew=line.split(',')
        
        if vnew not in header:
            content=content.replace(v,vnew)
        

    copyfile(file, file+'.bak')
    with open(file,'w') as f:
        f.write(content)

chdir(dir_bak)

