#!/usr/bin/env python

import sys

if len(sys.argv)==1 or sys.argv[1] in ['-h','--help']:
    print(f'Usage: {__file__} actirec01.csv')
    exit()

print('Checking', sys.argv[1])

with open(sys.argv[1]) as f:
    lines=f.read().strip().split('\n')

dict1={}

for line in lines:
    if line in dict1:
        dict1[line]+=1
    else:
        dict1[line]=1

print(' # : Line')
for line in dict1:
    if dict1[line]>1:
        print('{:2} : {}'.format(dict1[line], line))

print()
        
