#!/usr/bin/env python

import pandas as pd
import sys
from shutil import move

# sys.argv[1]=/path/to/pmod01_definitions.csv
# sys.argv[2]=chrpas (prefix)
df=pd.read_csv(sys.argv[1])

for i,row in df.iterrows():
    aliases=row['Aliases']

    if pd.isna(aliases):
        continue

    for v in aliases.split(','):
        if f'{sys.argv[2]}_' in v:
            print(f"'{v}',",end='')
            
            # replace it in definitions
            df.loc[i,'ElementName']=v

            # each cell has one relevant alias
            # so it is safe to break out
            break

print('')
move(sys.argv[1],sys.argv[1]+'.orig')
df.to_csv(sys.argv[1],index=False)

