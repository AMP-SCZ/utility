#!/usr/bin/env python

from datetime import datetime
import sys
import argparse
from os import remove,getcwd,chdir
import json
from tempfile import mkstemp
import pandas as pd
from glob import glob
from os.path import basename,abspath


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
    if interview_date=='':
        # no data in this form
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

    for v in columns:
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

            elif definition.loc[v,'DataType']=='String':
                if value in ['-3','-9']:
                    value=''
    
                size=definition.loc[v,'Size']
                if size:
                    value=value[:int(size)]

            elif definition.loc[v,'DataType']=='Date':
                value=nda_date(value)

            if definition.loc[v,'DataType']=='Float':
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
        df.at[row,'ampscz_missing_spec']=get_value(f'{prefix}_missing_spec',f'{event}_arm_{arm}')[1]
    else:
        df.at[row,'ampscz_missing_spec']=''

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
    with open(args.dict) as f:
        title,df=f.read().split('\n',1)

        prefix=args.prefix
        event=args.event

        columns=['subjectkey','src_subject_id','interview_date','interview_age','sex',
            'chrcssrsb_si1l','chrcssrsb_si2l','chrcssrsb_si3l','chrcssrsb_si4l','chrcssrsb_si5l','chrcssrsb_sidfrql','chrcssrsb_siddurl','chrcssrsb_sidctrl','chrcssrsb_siddtrl','chrcssrsb_sidrsnl','chrcssrsb_sb1l','chrcssrsb_sb3l','chrcssrsb_sb4l','chrcssrsb_sb5l','chrcssrsb_cssrs_mlmrllt1','chrcssrsb_cssrs_plmrlt1','chrcssrsb_cssrs_mlmlllt1','chrcssrsb_cssrs_plmllt1','chrcssrsb_actlthl3','chrcssrsb_potlthl3','chrcssrsb_css_sim1','chrcssrsb_css_sim2','chrcssrsb_css_sim3','chrcssrsb_css_sim4','chrcssrsb_css_sim5','chrcssrsb_css_sipmfreq','chrcssrsb_css_sipmdur','chrcssrsb_css_sipmctrl','chrcssrsb_css_sipmdet','chrcssrsb_css_sipmreas','chrcssrsb_idintsvl','chrcssrsb_cssrs_actual','chrcssrsb_snmacatl','chrcssrsb_sbnssibl','chrcssrsb_cssrs_nssi','chrcssrsb_cssrs_yrs_ia','chrcssrsb_nminatl','chrcssrsb_cssrs_yrs_pab','chrcssrsb_nmapab','chrcssrsb_cssrs_yrs_aa','chrcssrsb_nmabatl','chrcssrsb_css_sipmms',
            'ampscz_missing','ampscz_missing_spec']
        
        # save the remaining template
        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(','.join(columns))
        
        # load template as DataFrame
        df=pd.read_csv(name)
        columns=df.columns.values
        remove(name)
        
        # load template definition
        definition=pd.read_csv(args.dict.replace('_template','_definitions'))
        definition.set_index('ElementName',inplace=True)

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
    
    with open(args.output,'w') as f:
        f.write(title+'\n'+data)
    
    print('Generated',abspath(args.output))
    
