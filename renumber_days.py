#!/usr/bin/env python

import sys

if len(sys.argv)==1 or sys.argv[1]=='-h' or sys.argv[1]=='--help':
    print("""Usage:
./{__file__} combined-AMPSCZ-flowtest-day1to1.csv
Re-numbers the day column in a DPdash CSV file.
""")
    exit()

with open(sys.argv[1]) as f:
    content=f.read().strip().split('\n')
    
for i,line in enumerate(content):
    if i==0:
        continue
    
    day,rest=line.split(',',1)

    if i==int(day):
        continue
    else:
        content[i]=f'{i},'+rest

    
with open(sys.argv[1],'w') as f:
    f.write('\n'.join(content))

