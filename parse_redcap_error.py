#!/usr/bin/env python

import sys
from glob import glob

files=glob(sys.argv[1])

for file in files:

    with open(file) as f:
        content=f.read().split('\n')

    print('\033[92m','Parsing',file,'\033[0m')

    for i,line in enumerate(content):
        if 'HTTP Status: 400' in line:
            print(content[i-1])
            print(content[i+1])
            print('')
            print('')
        
