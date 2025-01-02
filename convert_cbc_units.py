#!/usr/bin/env python

import pandas as pd
import sys
from glob import glob
from os import getcwd, chdir

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
    {__file__} /mnt/prescient/RPMS_incoming/''')
    exit(0)

print("\nConvert PRESCIENT CBC form units to that of ProNET's\n")

dir_bak=getcwd()
chdir(sys.argv[1])

file=glob('PrescientStudy_Prescient_cbc_with_differential_*.csv')[0]
df=pd.read_csv(file,dtype=str)
df1=df.copy()

for c in 'chrcbc_hct chrcbc_hct_high chrcbc_hct_low'.split():
    print(c)
    df1[c]=df[c].apply(lambda x: round(100*float(x),2))

for c in 'chrcbc_hgb chrcbc_hgb_high chrcbc_hgb_low \
chrcbc_mchc chrcbc_mchc_high chrcbc_mchc_low'.split():
    print(c)
    df1[c]=df[c].apply(lambda x: round(1/10*float(x),2))


df1.to_csv(file,index=False)

chdir(dir_bak)

