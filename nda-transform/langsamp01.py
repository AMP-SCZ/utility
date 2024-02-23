#!/usr/bin/env python

from datetime import datetime
import sys
import argparse
from os import remove,getcwd,chdir
import json
from tempfile import mkstemp
import pandas as pd
from glob import glob
from os.path import isfile,basename,abspath,join as pjoin
import re


# this function should have knowledge of dict1
def get_value(var,event):

    for d in dict1:
        if d['redcap_event_name']==event:
            try:
                return d[var]
            except KeyError:
                return ''
                
    # the subject has not reached the event yet
    return ''
    

def months_since_consent(interview,consent):
    age= datetime.strptime(interview,'%Y-%m-%d')-datetime.strptime(consent,'%Y-%m-%d')
    return round(age.days/30)

def days_since_consent(interview,consent):
    age= datetime.strptime(interview,'%Y-%m-%d')-datetime.strptime(consent,'%Y-%m-%d')
    return age.days


def nda_date(redcap_date):
    if redcap_date=='':
        # REDCap missing: 1909-09-09
        # REDCap N/A: 1903-03-03
        return '03/03/1903'

    Y=redcap_date[:4]
    m,d=redcap_date[5:].split('-')
    new_date=f'{m}/{d}/{Y}'

    return new_date


def populate():

    src_subject_id=basename(file).split('.')[0]
    try:
        dfshared.loc[src_subject_id]
    except KeyError:
        return


    if dfshared.loc[src_subject_id,'phenotype']=='CHR':
        arm=1
    else:
        arm=2


    interview_date=get_value(f'{prefix}_interview_date',f'{event}_arm_{arm}')
    if interview_date in ['','-3','1903-03-03','-9','1909-09-09']:
        # no data in this form
        return

    try:
        # [] around index is required to make the resultant a DataFrame
        metadata=data.loc[[(src_subject_id,interview_type)]].values[0]
        study,nearest_day,session=metadata

        found=True
        transcript_=f'{study}/processed/{src_subject_id}/interviews/{interview_type}/transcripts/{study}_{src_subject_id}_interviewAudioTranscript_{interview_type}_day{nearest_day:04}_session{session:03}_REDACTED.txt'
        if not isfile(transcript_):
            
            transcript_=f'{study}/processed/{src_subject_id}/interviews/{interview_type}/transcripts/{study}_{src_subject_id}_interviewAudioTranscript_{interview_type}_day{-nearest_day:04}_session{session:03}_REDACTED.txt'
            if not isfile(transcript_):
                print(transcript_, '\033[0;31m could not be found\033[0m')
                found=False
        
    except KeyError:
        return


    # get shared variables
    df.at[row,'src_subject_id']=src_subject_id
    for v in ['subjectkey','sex']:
        df.at[row,v]=dfshared.loc[src_subject_id,v]


    # get form specific variables
    df.at[row,'interview_date']=nda_date(interview_date)
    
    chric_consent_date=get_value('chric_consent_date',f'screening_arm_{arm}')
    months=months_since_consent(interview_date,chric_consent_date)
    df.at[row,'interview_age']=dfshared.loc[src_subject_id,'interview_age']+months

    for v in run_sheet_vars:
        if prefix in v:
            value=get_value(v,f'{event}_arm_{arm}')
            
            vrange=definition.loc[v,'ValueRange']
            if not pd.isna(vrange):
                if '-300' in vrange or '-900' in vrange:
                    # NDA missing: -900
                    # NDA N/A: -300
                    if value=='-3':
                        value='-300'
                    elif value=='-9':
                        value='-900'

            if definition.loc[v,'DataType']=='Integer':
                try:
                    value=int(value)
                except ValueError:
                    value=''

            elif definition.loc[v,'DataType']=='String':
                if value in ['-3','-9']:
                    value=''
    
                size=definition.loc[v,'Size']
                if size:
                    value=value[:int(size)]

            elif definition.loc[v,'DataType']=='Date':
                value=nda_date(value)

            elif definition.loc[v,'DataType']=='Float':
                try:
                    value=round(float(value),3)
                except ValueError:
                    pass

            df.at[row,v]=value


    missing=get_value(f'{prefix}_missing',f'{event}_arm_{arm}')
    if missing=='':
        # not clicked
        missing='0'
    df.at[row,'ampscz_missing']=missing
    if missing=='1':
        value=get_value(f'{prefix}_missing_spec',f'{event}_arm_{arm}')
        
        if len(value)>1:
            # two letter missing codes: W1,W2,W3,... M1,M2,M3,...
            df.at[row,'ampscz_missing_spec']=value[1]
        else:
            # single number missing code: 1,2,3,...
            df.at[row,'ampscz_missing_spec']=value

    else:
        df.at[row,'ampscz_missing_spec']=''


    # Example paths:
    # PronetOR/processed/OR10684/interviews/open/OR10684_open_combinedQCRecords.csv
    # PrescientSG/processed/SG99731/interviews/psychs/SG99731_psychs_combinedQCRecords.csv

    _root=pjoin(file.split('surveys')[0], 'interviews', interview_type)
    features_file=pjoin(_root, f'{src_subject_id}_{interview_type}_combinedQCRecords.csv')

    if not isfile(features_file):
        return

    
    print('\tProcessing',features_file)

    dfavl=pd.read_csv(features_file)
    
    if found:
        df.at[row,'transcript_file']=abspath(transcript_).split('/processed/')[-1]


    for i,_row in dfavl.iterrows():
        if _row['day']==nearest_day:

            total_words=sum(_row[t] for t in 'num_words_S1,num_words_S2,num_words_S3'.split(','))

            for v in avl_vars:
                if v=='num_turns_total':
                    value=sum(_row[t] for t in 'num_turns_S1,num_turns_S2,num_turns_S3'.split(','))
                
                elif v=='num_words_s1':
                    value=_row['num_words_S1']

                elif v=='num_words_s2':
                    value=_row['num_words_S2']

                elif v=='num_words_s3':
                    value=_row['num_words_S3']
                
                elif v=='interview_type':
                    if _row[v]=='open':
                        value=1
                    elif _row[v]=='psychs':
                        value=2

                elif v in 'num_inaudible,num_redacted':
                    value=round(_row[v]/total_words*100,3)

                else:
                    value=_row[v]
                
                if definition.loc[v,'DataType']=='Integer':
                    if not pd.isna(value):
                        value=int(value)

                df.at[row,v]=value
            
            break
        else:
            print('\033[0;31m',features_file,nearest_day,'\033[0m')
    
    # return df


if __name__=='__main__':

    parser= argparse.ArgumentParser("Make data frame to submit to NDA")
    parser.add_argument("--dict", required=True,
        help="/path/to/nda/submission/template.csv")
    parser.add_argument("--root", required=True,
        help="/path/to/PHOENIX/GENERAL/")
    parser.add_argument("-t","--template", required=True,
        help="*/processed/*/surveys/*.Pronet.json")
    parser.add_argument("-o","--output", required=True,
        help="/path/to/submission_ready.csv")
    parser.add_argument("-e","--event", required=True,
        help="Event name: screening, baseline, month_1, etc.")
    parser.add_argument("--data", required=True,
        help="/path/to/data01*.csv containing non-survey data e.g. actirec01, image03")
    parser.add_argument("-p","--prefix", required=True,
        help="Variable name prefix e.g. chrnsipr, chrpgis, chrassist, etc.")
    parser.add_argument("--shared", required=True,
        help="/path/to/ndar_subject01*.csv containing fields shared across NDA dicts")

    
    args= parser.parse_args()
    
    # load shared ndar_subject01
    with open(args.shared) as f:
        title,df=f.read().split('\n',1)

        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(df)
        
        dfshared=pd.read_csv(name)
        remove(name)
        dfshared.set_index('src_subject_id',inplace=True)
    
    
    # load NDA dictionary
    args.dict=args.dict.replace('_template.csv','_definitions.csv')
    title=re.search('/(.+?)01_definitions.csv',args.dict).group(1)
    definition=pd.read_csv(args.dict)
    definition.set_index('ElementName',inplace=True)
    
    prefix=args.prefix
    event=args.event

    if prefix=='chrspeech':
        interview_type='open'
    elif prefix=='chrpsychs_av':
        interview_type='psychs'

    columns=['subjectkey','src_subject_id','interview_date','interview_age','sex']
    # run sheet vars
    run_sheet_vars=[]
    for c in definition.index:
        if prefix in c:
            run_sheet_vars.append(c.strip())
    
    # audio/video/transcript vars
    avl_vars='interview_type,interview_number,length_minutes,final_timestamp_minutes,overall_db,num_redacted,num_inaudible,num_subjects,num_words_s1,num_words_s2,num_words_s3,num_turns_total'.split(',')

    columns=columns+run_sheet_vars+avl_vars+['transcript_file','ampscz_missing','ampscz_missing_spec']
    
    data=pd.read_csv(args.data)
    data.set_index(['subject','interview_type'],inplace=True)


    # save the remaining template
    _,name=mkstemp()
    with open(name,'w') as fw:
        fw.write(','.join(columns))
    
    # load template as DataFrame
    df=pd.read_csv(name)
    columns=df.columns.values
    remove(name)


    dir_bak=getcwd()
    chdir(args.root)
    
    files=glob(args.template)
    for row,file in enumerate(files):
        
        print('Processing',file)
        
        with open(file) as f:
            dict1=json.load(f)

        populate()


    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    chdir(dir_bak)
    
    _,name=mkstemp()
    df.to_csv(name,index=False)
    
    with open(name) as f:
        data=f.read()
    remove(name)
    
    
    args.output=args.output.replace('.csv',f'_{interview_type}.csv')
    with open(args.output,'w') as f:
        f.write(title+',01'+'\n'+data)
    
    print('Generated',abspath(args.output))
    
