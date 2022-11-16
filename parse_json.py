#!/usr/bin/env python

from os import environ, getcwd, chdir
environ['OPENBLAS_NUM_THREADS']='16'

from glob import glob
import json,sys
import pandas as pd
from os.path import abspath
import yaml

if len(sys.argv)<3 or sys.argv[1]=='-h' or sys.argv[1]=='--help':
    print(f"""A command line program for making REDCap-like reports.
Usage:
{__file__} /path/to/event_var.yaml /path/to/Network/PHOENIX/PROTECTED
{__file__} /path/to/event_var.yaml /path/to/Network/PHOENIX/PROTECTED */raw/*/surveys/*.Pronet.json
The last template is optional.
Sample yaml file:

screening_arm_1:
    - chrguid_guid
    - chrhealth_alle

baseline_arm_1:
    - chrdemo_age_mos_chr

baseline_arm_2:
    - chrdemo_age_mos_hc

""")
    exit(0)


with open(sys.argv[1]) as f:
    rows=yaml.safe_load(f)

dir_bak=getcwd()
chdir(sys.argv[2])

template='*/raw/*/surveys/*.Pronet.json'
if len(sys.argv)==4:
    template=sys.argv[3]

files=glob(template)

L=len(files)
values={}
for event,vars in rows.items():
    values[event]={}
    for v in vars:
        values[event][v]=['']*L

for i,file in enumerate(files):
    with open(file) as f:
        dict1=json.load(f)

    print(file)

    for event,vars in rows.items():

        print('\t',event)

        for v in vars:

            print('\t\t',v)

            for d in dict1:
                if d['redcap_event_name']==event:
                    values[event][v][i]=d['chric_record_id']+' '+d[v]
                    break
    print('\n')


print('\n\n')

for event,vars in rows.items():
    for v in vars:
        print('Report of',event,v)
        print('=====================')
        for i in range(L):
            print(values[event][v][i])

        print('=====================\n')


chdir(dir_bak)

