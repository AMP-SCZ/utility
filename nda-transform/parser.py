#!/usr/bin/env python

import pandas as pd

_df=pd.read_csv('NDA_RELEASE_4_ALL_sample_types.csv',dtype=str)

# skip the negative days
filtered=[]
for i,row in _df.iterrows():
    if 'day-' not in row['day']:
        filtered.append(_df.loc[i])

df=pd.DataFrame(filtered,columns=_df.columns)

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


def print_group(_g):

    for k in _g.groups:
        print(_g.get_group(k))

groups1= df.groupby(['src_subject_id', 'interview_type'])
for g1 in groups1.groups:
    if 'diary' in g1:
        continue

    group1= groups1.get_group(g1)

    groups2= group1.groupby('day')

    if ('open' in g1 and len(groups2)>2) or \
        ('psychs' in g1 and len(groups2)>10):
        # print_group(groups2)
        print(g1,[k for k in groups2.groups])
        continue
        
    for i,g2 in enumerate(groups2.groups):

        num_sessions=len(groups2.groups[g2])
        
        for j in range(num_sessions):
            f.write(f'{g1},{g2},{events[g1[1]][i]}\n')

f.close()


