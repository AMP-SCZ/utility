#!/usr/bin/env python

import sys

with open(sys.argv[1]) as f:
    content=f.read().split('\n')

print('\033[92m','Parsing', sys.argv[1],'\033[0m')

for i,line in enumerate(content):
    if 'HTTP Status: 400' in line:
        print(content[i-1])
        print(content[i+1])
        print('')
        print('')
        
