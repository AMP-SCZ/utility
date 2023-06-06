#!/usr/bin/env python

import pandas as pd
import sys

# sys.argv[1]=/path/to/pmod01_definitions.csv
# sys.argv[2]=chrpas (prefix)
df=pd.read_csv(sys.argv[1])


for a in df['ElementName'].values:
    
    if f'{sys.argv[2]}_' in a:
        print(a)

print('')

