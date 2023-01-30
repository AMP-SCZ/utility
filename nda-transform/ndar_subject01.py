#!/usr/bin/env python

from datetime import datetime
import sys
import argparse
from os import remove,getcwd,chdir
import json
from tempfile import mkstemp
import pandas as pd
from glob import glob


# this function should have knowledge of dict1
def get_value(var,event):

    for d in dict1:
        if d['redcap_event_name']==event:
            return d[var]



def populate():

    chrcrit_part=get_value('chrcrit_part','screening_arm_1')
    arm=1
    phenotype='CHR'
    phenotype_description='CHR Participant'
    if not chrcrit_part:
        chrcrit_part=get_value('chrcrit_part','screening_arm_2')
        
        if not chrcrit_part:
            return
            
        arm=2
        phenotype='HC'
        phenotype_description='Healthy Control Participant'

    twins_study='No'
    sibling_study='No'
    family_study='No'
    sample_taken='No'
    
    subjectkey=get_value('chrguid_guid',f'screening_arm_{arm}')
    if not subjectkey.startswith('NDAR'):
        # we cannot submit a subject w/o a valid GUID
        return

    src_subject_id=get_value('chric_record_id',f'screening_arm_{arm}')


    if arm==1:
        interview_age=get_value('chrdemo_age_mos_chr','baseline_arm_1')
    elif arm==2:
        interview_age=get_value('chrdemo_age_mos_hc','baseline_arm_2')
    
    if interview_age=='' or interview_age==None:
         # we cannot submit a subject w/o an age
        return

        
    sex=get_value('chrdemo_sexassigned',f'baseline_arm_{arm}')
    sex='M' if sex=='1' else 'F'

    race_to_nda={
        1:'American Indian/Alaska Native',
        2:'Asian',
        3:'Asian',
        4:'Asian',
        5:'Black or African American',
        6:'White',
        7:'White',
        8:'Hawaiian or Pacific Islander',
    }

    _races=[]
    for i in range(1,9):
        bit=get_value(f'chrdemo_racial_back___{i}',f'baseline_arm_{arm}')
        if bit=='1':
            _races.append(race_to_nda[i])

    reported=len(_races)
    if reported>1:
        race='More than one race'
    elif reported==0:
        race='Unknown or not reported'
    else:
        race=_races[0]


    interview_date=get_value('chric_consent_date',f'screening_arm_{arm}')
    interview_date=datetime.strptime(interview_date,'%Y-%m-%d').strftime('%m/%d/%Y')
    
    for c in df.columns:
        df.at[row,c]=eval(c)

    # df.at[row,["subjectkey","src_subject_id","interview_date","interview_age","sex","race","phenotype","phenotype_description","twins_study","sibling_study","family_study","sample_taken"]]=[subjectkey,src_subject_id,interview_date,interview_age,sex,race,phenotype,phenotype_description,twins_study,sibling_study,family_study,sample_taken]


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
    
    args= parser.parse_args()

    
    # load NDA dictionary
    with open(args.dict) as f:
        title,df=f.read().split('\n',1)
       
        columns=["subjectkey","src_subject_id","interview_date","interview_age","sex",
            "race","phenotype","phenotype_description",
            "twins_study","sibling_study","family_study","sample_taken"]
        
        df=pd.DataFrame(columns=columns)


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
    print(df[["subjectkey","src_subject_id","interview_date","interview_age","sex","race","phenotype"]])

    chdir(dir_bak)
    
    _,name=mkstemp()
    df.to_csv(name,index=False)
    
    with open(name) as f:
        data=f.read()
    remove(name)
    
    with open(args.output,'w') as f:
        f.write(title+'\n'+data)
    

