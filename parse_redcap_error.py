#!/usr/bin/env python

import sys
from glob import glob
import re

files=glob(sys.argv[1])

for file in files:

    with open(file) as f:
        content=f.read().strip().split('\n')

    print('\033[92m','Parsing',file,'\033[0m')

    if file.endswith('.out'):
        for i,line in enumerate(content):
            if 'HTTP Status: 400' in line:
                print(content[i-1])
                print(content[i+1])
                print('')
                print('')


    elif file.endswith('.err'):
        i=0
        while i<len(content):
            if '\033[0;31m' not in content[i]:
                print(content[i-1])

                while '\033[0;31m' not in content[i]:
                    print(content[i])
                    i+=1
                    if i==len(content):
                        break
                print('')
                print('')
                
            i+=1

