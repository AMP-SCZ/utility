#!/usr/bin/env python

import sys

if sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {__file__} /path/to/email
The 'email' is a text file containing Rachel Bleggi (UNC)'s email with site and rack codes.
It is in the following format:
SITE
CODES
<br>
SITE
CODES
<br>
...
...

Given 'email', this script will print commands that can be readily run to generate
blood saliva manifests. It basically automates the work needed to formulate
sort_blood_saliva_rack.sh commands.''')
    exit(0)

with open(sys.argv[1]) as f:
    lines=f.read().strip().split('\n')

i=0
n_site=0
n_rack=0
while i<len(lines):
    site=lines[i].strip()

    # Rachel prepends * for repeated sites
    if site[0]=='*':
        site=site[1:]

    codes=lines[i+1].strip()
    print(f'./sort_blood_saliva_rack.sh -n Pronet -s {site} -c \"{codes}\" && sleep 60')
    i+=3
    n_rack+=len(codes.split())
    n_site+=1

print('\nTotal sites:',n_site,'- total racks:',n_rack)

