#!/usr/bin/env python

import pandas as pd
import json
import numpy as np
from os import getcwd, chdir, makedirs, stat
from os.path import dirname, basename, abspath
from datetime import datetime, timedelta
import sys
from glob import glob
from multiprocessing import Pool
import signal
from hashlib import md5

# Shift REDCap dates by one of [-14,-7,7,14] randomly chosen days
# Usage:
# __file__ NDA_ROOT "Pronet/PHOENIX/PROTECTED/*/raw/*/surveys/*.Pronet.json"
# __file__ PHOENIX_PROTECTED "*/raw/*/surveys/*.Pronet.json"

_shift= [-14,-7,7,14]
L= len(_shift)
prob= [1/L]*L

dir_bak=getcwd()
chdir(sys.argv[1])

files=glob(sys.argv[2])
dfshift=pd.read_csv('date_offset.csv')
dfshift.set_index('subject',inplace=True)


for file in files:
    subject=basename(file).split('.')[0]
    
    with open(file) as f:
        content= f.read()
    curr_hash= md5(content.encode('utf-8')).hexdigest()

    try:
        dfshift.loc[subject]
    except:
        # date shift setter
        print('New subject', subject)

        # randomize according to multinomial distribution
        shift= _shift[np.where(np.random.multinomial(1,prob))[0][0]]
        dfshift.at[subject,'days']=shift
        # always upload new subjects
        dfshift.loc[subject]=[shift,curr_hash,1]
        continue


    # changed determiner
    if dfshift.loc[subject,'stat_hash']!=curr_hash:
        # store the new hash
        dfshift.at[subject,'stat_hash']=curr_hash
        # and flag it for upload to REDCap
        dfshift.at[subject,'upload']=1
    else:
        dfshift.at[subject,'upload']=0
        print(file, 'has not been modified, skipping')


dfshift= dfshift.astype({'days':'short','stat_hash':str,'upload':'short'})
dfshift.sort_index(inplace=True)
pd.set_option("display.max_rows", None)
print(dfshift)
dfshift.to_csv('date_offset.csv')

chdir(dir_bak)


