#!/usr/bin/env python

from shutil import move
from yaml import safe_load
from glob import glob
from datetime import date
from os import getcwd, chdir, environ
from os.path import isfile, dirname
import sys


suffix=date.today().strftime('%d.%m.%Y.csv')

with open(dirname(__file__)+'/rename_RPMS_vars.yaml') as f:
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

    
    with open(file) as f:
        content=f.read()
        # we need only 1 split
        header,data=content.split('\n',1)
        
    
    for line in dict1[pattern]:
        v,vnew=line.split(',')
        # stricten the patterns
        v=f',{v},'
        vnew=f',{vnew},'
        
        if vnew not in header:
            # we know that v occurs only once in the header
            # the 1 should prevent search over the entire header
            # and thereby increase speed
            header=header.replace(v,vnew,1)

    content=header+'\n'+data

    move(file, file+'.bak')
    with open(file,'w') as f:
        f.write(content)

chdir(dir_bak)

