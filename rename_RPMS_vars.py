#!/usr/bin/env python

from shutil import copyfile
from yaml import safe_load
from glob import glob
from datetime import date

suffix=date.today().strftime('%d.%m.%Y.csv')

with open('rename_RPMS_vars.yaml') as f:
    dict1=safe_load(f)
    
for prefix in dict1.keys()
    file=prefix+suffix
    
    with open(file) as f:
        content=f.read()
        
    
    for line in dict1[k]:
        v,vnew=line.split()
        
        content=content.replace(v,vnew)
        

copyfile(file, file+'.bak')
with open(file,'w') as f:
    f.write(content)

