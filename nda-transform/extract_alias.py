#!/usr/bin/env python

import pandas as pd
import sys

# sys.argv[1]=/path/to/pmod01_definitions.csv
# sys.argv[2]=chrpas (prefix)
df=pd.read_csv(sys.argv[1])


for a in df['Aliases'].values:
    if pd.isna(a):
        continue

    for v in a.split(','):
        if f'{sys.argv[2]}_' in v:
            print(v)

