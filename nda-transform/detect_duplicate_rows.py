#!/usr/bin/env python

import sys
from glob import glob

if len(sys.argv)==1 or sys.argv[1] in ['-h','--help']:
    print(f"""Usage:
{__file__} actirec01.csv
{__file__} /path/to/*csv""")
    exit()


files=sys.argv[1:]
for file in files:
    print('Checking', file)

    with open(file) as f:
        lines=f.read().strip().split('\n')

    dict1={}

    duplicate=False
    for line in lines:
        if line in dict1:
            dict1[line]+=1
            duplicate=True
        else:
            dict1[line]=1
    
    if duplicate:
        print(' # : Line')

    for line in dict1:
        if dict1[line]>1:
            print('{:2} : {}'.format(dict1[line], line))

    print()
    
