#!/usr/bin/env python

import pandas as pd

df=pd.read_csv('NDA_RELEASE_4_ALL_sample_types.csv',dtype=str)
groups=df.groupby(['src_subject_id', 'interview_type', 'day'])

events={'open': ['baseline','month_2'],
    'psychs': ['screening',
        'baseline',
        'month_1',
        'month_2',
        'month_3',
        'month_6',
        'month_12',
        'month_18',
        'month_24',
        'conversion']
    }

f= open('trust_based_events.csv', 'w')

for g in groups.groups.keys():
    if 'diary' in g:
        continue 
    num_sessions=len(groups.groups[g])
    if 'open' in g and num_sessions>2:
        print(g,groups.groups[g])
        continue 
    elif 'psychs' in g and num_sessions>10:
        print(g,groups.groups[g])
        continue 
    for i in range(num_sessions):
        f.write(f'{g},{events[g[1]][i]}\n')

f.close()


