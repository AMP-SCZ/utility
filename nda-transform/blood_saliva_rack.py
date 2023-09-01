#!/usr/bin/env python

from datetime import datetime
import sys
import argparse
from os import remove,getcwd,chdir
import json
from tempfile import mkstemp
import pandas as pd
from glob import glob
from os.path import isfile,basename,abspath,dirname,join as pjoin


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
        return '1903-03-03'

    Y=redcap_date[:4]
    m,d=redcap_date[5:].split('-')
    new_date=f'{m}/{d}/{Y}'

    return new_date


matcode_var={
    'WB': 'chrblood_wb1id chrblood_wb1pos chrblood_wb2id chrblood_wb2pos chrblood_wb3id chrblood_wb3pos',
    'SE': 'chrblood_se1id chrblood_se1pos chrblood_se2id chrblood_se2pos chrblood_se3id chrblood_se3pos',
    'PL': 'chrblood_pl1id chrblood_pl1pos chrblood_pl2id chrblood_pl2pos chrblood_pl3id chrblood_pl3pos',
    'BC': 'chrblood_bc1id chrblood_bc1pos chrblood_bc1box',
    'S': 'chrsaliva_id1a chrsaliva_pos1a chrsaliva_box1a chrsaliva_id1b chrsaliva_pos1b chrsaliva_box1b '+ \
         'chrsaliva_id2a chrsaliva_pos2a chrsaliva_box2a chrsaliva_id2b chrsaliva_pos2b chrsaliva_box2b'
}


def populate(i):

    src_subject_id=basename(file).split('.')[0]
    try:
        dfshared.loc[src_subject_id]
    except KeyError:
        return i


    if dfshared.loc[src_subject_id,'phenotype']=='CHR':
        arm=1
        cohort='CHR'
    else:
        arm=2
        cohort='HC'


    # get shared variables
    subjectkey=dfshared.loc[src_subject_id,'subjectkey']
    sex=dfshared.loc[src_subject_id,'sex']


    chric_consent_date=get_value('chric_consent_date',f'screening_arm_{arm}')


    for matcode in 'WB SE PL BC'.split():
        v1=matcode_var[matcode]
        
        if get_value('chrblood_missing',f'{event}_arm_{arm}')=='1':
            # no data in this form
            continue
            
        draw_date=get_value('chrblood_drawdate',f'{event}_arm_{arm}')
        if len(draw_date)<10:
            continue
        else:
            draw_date=draw_date[:10]

        # calculate age on draw_date
        months=months_since_consent(draw_date,chric_consent_date)
        interview_age=dfshared.loc[src_subject_id,'interview_age']+months
        
        rack_code=get_value('chrblood_rack_barcode',f'{event}_arm_{arm}')
        if matcode=='BC':
            rack_code=get_value('chrblood_bc1box',f'{event}_arm_{arm}')

        # deal with people's state of minds
        rack_code=rack_code.strip()
        if rack_code in ['-3','-9']:
            print('Blood rack code',rack_code)
            continue
        
        for j,v in enumerate(v1.split()):
            value=get_value(v,f'{event}_arm_{arm}')
            if j%2==0:
                inventory_code=value
            else:
                pos_on_rack=value
                
                df.loc[i]=[rack_code,pos_on_rack,draw_date,inventory_code,matcode,src_subject_id,cohort,
                    sex,interview_age,'Months',subjectkey]
                i+=1
    


    if get_value('chrsaliva_missing',f'{event}_arm_{arm}')=='1':
        # no data in this form
        return i
    
    # repeat the above for saliva
    for matcode in 'S'.split():
        v1=matcode_var[matcode]
        
        draw_date=get_value('chrsaliva_coldate',f'{event}_arm_{arm}')
        if len(draw_date)<10:
            continue
            
        # calculate age on draw_date
        months=months_since_consent(draw_date,chric_consent_date)
        interview_age=dfshared.loc[src_subject_id,'interview_age']+months
        
        
        for j,v in enumerate(v1.split()):
            value=get_value(v,f'{event}_arm_{arm}')
            if j%3==0:
                inventory_code=value
            elif j%3==1:
                pos_on_rack=value
            elif j%3==2:
                rack_code=value

                # deal with people's state of minds
                rack_code=rack_code.strip()
                if rack_code in ['-3','-9']:
                    print('Saliva rack code',rack_code)
                    continue

                if rack_code[:6].lower()=='pronet':
                    rack_code='ProNET-'+rack_code.strip()[-4:]

                
                df.loc[i]=[rack_code,pos_on_rack,draw_date,inventory_code,matcode,src_subject_id,cohort,
                    sex,interview_age,'Months',subjectkey]
                i+=1


    return i



if __name__=='__main__':

    parser= argparse.ArgumentParser("Make data frame to submit to NDA")
    parser.add_argument("--root", required=True,
        help="/path/to/PHOENIX/GENERAL/")
    parser.add_argument("-o","--output", required=True,
        help="/path/to/submission_ready.csv")
    parser.add_argument("-t","--template", required=True,
        help="*/processed/*/surveys/*.Pronet.json")
    parser.add_argument("-e","--event", required=True,
        help="Event name: screening, baseline, month_1, etc.")
    parser.add_argument("--shared", required=True,
        help="/path/to/ndar_subject01*.csv containing fields shared across NDA dicts")

    
    args= parser.parse_args()
    event=args.event
        
    # load shared ndar_subject01
    with open(args.shared) as f:
        title,df=f.read().split('\n',1)

        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(df)
        
        dfshared=pd.read_csv(name)
        remove(name)
        dfshared.set_index('src_subject_id',inplace=True)
    
    
    _columns='Rack Code,Position on Rack,Draw Date,Inventory Code,Matcode,'+ \
             'AMPSCZ_ID,Cohort,Sex,Age on Draw Date,Age Unit,GUID'
    df=pd.DataFrame(columns=_columns.split(','))
    i=0


    dir_bak=getcwd()
    chdir(args.root)
    
    files=glob(args.template)

    for row,file in enumerate(files):
        
        print('Processing',file)
        
        with open(file) as f:
            dict1=json.load(f)

        i=populate(i)


    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    chdir(dir_bak)
    
    df.to_csv(args.output,index=False)
    
    print('Generated',abspath(args.output))

