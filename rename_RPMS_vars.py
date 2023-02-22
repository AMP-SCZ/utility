#!/usr/bin/env python

from shutil import move
from yaml import safe_load
from glob import glob
from datetime import date
from os import getcwd, chdir, environ
from os.path import isfile, dirname
import sys

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
    {__file__} /mnt/prescient/RPMS_incoming/
    {__file__} /mnt/prescient/RPMS_incoming/ 31.12.2022.csv
    {__file__} /mnt/prescient/RPMS_incoming/ 31.12.2022.csv /path/to/rename_RPMS_vars.yaml
First arg is mandatory, rest are optional.''')
    exit(0)

try:
    suffix=sys.argv[2]
except:
    suffix=date.today().strftime('%d.%m.%Y.csv')

try:
    yaml_file=sys.argv[3]
except:
    yaml_file=dirname(__file__)+'/rename_RPMS_vars.yaml'

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
    
    with open(file) as f:
        content=f.read()
        # we need only 1 split
        header,data=content.split('\n',1)
        

    replace=0
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
            replace=1


    # replace the file if any header has been renamed
    if replace:
        content=header+'\n'+data

        # move(file, file+'.bak')
        with open(file,'w') as f:
            f.write(content)

chdir(dir_bak)

print('')

