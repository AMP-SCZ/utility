#!/usr/bin/env python

import sys

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
        
