#!/usr/bin/env python

from glob import glob
from hashlib import md5
from os.path import abspath, basename, dirname, isfile, join as pjoin
from time import sleep
from shutil import move
from glob import iglob
import sys
import numpy as np
from pickle import UnpicklingError

prefix= pjoin(abspath(dirname(__file__)),'.dpimport_hash')
hash_repo=prefix+'.npy'

# one hash repository is used for all data types i.e. importers
# when one importer is modifying it, others cannot use it
# so during its use, rename it as .dpimport_hash.npy.lock
while 1:
    if not(isfile(hash_repo)):
        # it is being used by another importer
        # retry to read it after 5 minutes
        print(hash_repo,'could not be found at this time')
        print('\tgoing to sleep for 5 minutes ...')
        sleep(300)

    else:
        # rename it i.e. lock it to prevent others from accessing it
        hash_repo_locked=prefix+'.lock.npy'
        move(hash_repo,hash_repo_locked)
        try:
            hash_record=np.load(hash_repo_locked, allow_pickle=True).item()

        except UnpicklingError:
            # initial case
            hash_record={}

        # hash_record is a dictionary with key,value pairs
        # key=AB-AB12345-assessment
        # value=[hash,True/False]
        # True=modified since last read
        
        print('hash_record found, calculating and comparing hashes ...')
        
        break

for i,file in enumerate(iglob(sys.argv[1])):

    try:
        with open(file) as f:
            content=f.read().strip().encode('utf-8')

    except FileNotFoundError:
        print(file,'could not be read\n')
        continue

    hash=md5(content).hexdigest()
    
    key=basename(file)
    if key in hash_record:
        if hash_record[key][0]!=hash:
            hash_record[key][0]=hash
            hash_record[key][1]=True

            
    
    else:
        hash_record[key]=[hash,False]

    print(i,key,hash_record[key])

f.close()

print('hash calculation complete')

# now write back the hash_record and release the hash_repo
np.save(hash_repo_locked,hash_record)
move(hash_repo_locked,hash_repo)


