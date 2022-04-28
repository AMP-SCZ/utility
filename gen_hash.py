#!/usr/bin/env python

from hashlib import sha256
import sys
from os.path import abspath


if len(sys.argv)<3:
    print(f"""Usage:
{__file__} STUDY_metadata.csv assessment
STUDY_metadata.csv must contain columns:
    Subject ID,Active,Consent,Study

Example assessment names: flowcheck, interviewsMonoAudioQC, mriqc""")
    exit()

with open(abspath(sys.argv[1])) as f:
    ids=f.read().split('\n')

assessment= sys.argv[2]

ids= [i for i in ids if i and (i != 'Subject ID,Active,Consent,Study')]

for i in ids:
    e= i.split(',')
    name= e[-1]+ e[0]+ assessment
    
    # example name= "YAYA00015flowcheck"
    hash_mongo= sha256(name.encode()).hexdigest()

    print(hash_mongo)
