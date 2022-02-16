#!/usr/bin/env python

from hashlib import sha256
import sys
from os.path import abspath

assessment='flowcheck'

with open(abspath(sys.argv[1])) as f:
    ids=f.read().split('\n')

ids= [i for i in ids if i and (i != 'Subject ID,Active,Consent,Study')]

print(ids)

for i in ids:
    e= i.split(',')
    name= e[-1]+ e[0]+ assessment
    
    # example name= "YAYA00015flowcheck"
    hash_mongo= sha256(name.encode()).hexdigest()

    print(hash_mongo)
