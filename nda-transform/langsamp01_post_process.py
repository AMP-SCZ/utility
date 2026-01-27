#!/usr/bin/env python

import pandas as pd
import sys

df=pd.read_csv(sys.argv[1], dtype=str)
df1= df.copy()
import re

# rename columns
df1.rename(columns={'redcap_event_name':'visit','file_name.txt':'transcript_file'}, inplace=True)

# drop non-existent columns
df1.drop(['n_words','n_disfluencies_per_word'], axis=1, inplace=True)

# reshape interview dates to MM/DD/YYYY
df1.interview_date= df.interview_date.apply(lambda x: f'{x[5:7]}/{x[8:10]}/{x[0:4]}')

# make some columns integers
for c in """n_disfluencies
    n_false_starts
    n_word_repeats
    n_stutters
    n_non_verbal_fillers
    n_verbal_fillers""".split():
    
    df1[c]=df[c].apply(lambda x: str(int(float(x))) if not pd.isna(x) else '')


# change open/psychs/diary to 1/2/3
df1.interview_type= df.interview_type.map(lambda x: 1 if x=='open' \
    else 2 if x=='psychs' else 3 if x=='diary' else '')


# trim _arm_? from visit label
df1.visit= df.visit.map(lambda x: x.split('_arm_')[0])


# keep integer only from session???
df1.interview_number= df.interview_number.apply(lambda x: int(x[-3:]) if 'session' in x \
    else int(x[-1]) if 'submission' in x else '')


# use relative path for transcript_file

files=[]
for i,row in df.iterrows():
    file= row['file_name.txt']

    if not pd.isna(file):
        if 'Journal' in file:
            _file= '{}/phone/audio_journals/transcripts/{}'.format(
                row['src_subject_id'],file)
            # _file= re.sub(r'submission...',row['interview_number'],_file)
            files.append(_file)
            
        elif 'Transcript' in file:
            _file= '{}/interviews/{}/transcripts/{}'.format(
                row['src_subject_id'],row['interview_type'],file)
            files.append(_file)

    else:
        files.append('')

df1['transcript_file']=files


# change column order
begin='subjectkey,src_subject_id,interview_date,interview_age,sex,visit'.split(',')
for c in df1.columns:
    if c not in begin:
        begin.append(c)

df2= df1[begin]
# save the data back
df2.to_csv(sys.argv[1].strip('.dm1447'), index=False)


