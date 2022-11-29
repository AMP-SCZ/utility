#!/usr/bin/env python

from os import getcwd, chdir, environ
environ['OPENBLAS_NUM_THREADS']='16'
from os.path import join as pjoin

import pandas as pd
import json
from glob import glob
import sys


# Extract specified form entries from JSON and CSV files
# Usage:
# __file__ /path/to/*DataDictionary*csv /path/to/out/dir/


# input section ==================================================================

df=pd.read_csv(sys.argv[1],encoding='ISO-8859-1',on_bad_lines='skip',engine='python')

var_col='field_name'
form_col='form_name'
type_col='field_type'
value_col='text_validation_type_or_show_slider_number'

if var_col not in df:
    var_col='Variable / Field Name'
    form_col='Form Name'
    type_col='Field Type'
    value_col='Choices, Calculations, OR Slider Labels'

groups=df.groupby(form_col)


# input for experiment on 10/12/2022
# forms=['family_interview_for_genetic_studies_figs','psychs_p1p8','psychs_p9ac32','scid5_psychosis_mood_substance_abuse']
# types=['text', 'radio', 'checkbox', 'dropdown', 'yesno', 'calc']
# 
# json_event={'Pronet/PHOENIX/PROTECTED/PronetYA/raw/YA01508/surveys/YA01508.Pronet.json':
#             ['screening_arm_1','screening_arm_1','screening_arm_1','baseline_arm_1'],
#             'Pronet/PHOENIX/PROTECTED/PronetPI/raw/PI01355/surveys/PI01355.Pronet.json':
#             ['screening_arm_2','screening_arm_2','screening_arm_2','baseline_arm_2'],
#             'Pronet/PHOENIX/PROTECTED/PronetWU/raw/WU05257/surveys/WU05257.Pronet.json':
#             ['screening_arm_1','screening_arm_1','screening_arm_1','baseline_arm_1']}
# 
# rpms_dirs={'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME21922':[1,1,1,2],
#            'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME78581':[1,1,1,2],
#            'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME22598':[1,1,1,2]}



# input for experiment on 11/15/2022
# forms=['sofas_screening', 'scid5_schizotypal_personality_sciddpq']
# types=['text', 'radio', 'checkbox', 'dropdown', 'yesno']
# 
# json_event={'Pronet/PHOENIX/PROTECTED/PronetYA/raw/YA01508/surveys/YA01508.Pronet.json':
#             ['screening_arm_1','screening_arm_1'],
#             'Pronet/PHOENIX/PROTECTED/PronetPI/raw/PI01355/surveys/PI01355.Pronet.json':
#             ['screening_arm_2','screening_arm_2'],
#             'Pronet/PHOENIX/PROTECTED/PronetWU/raw/WU05257/surveys/WU05257.Pronet.json':
#             ['screening_arm_1','screening_arm_1']}
# 
# rpms_dirs={'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME21922':[1,1],
#            'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME78581':[1,1],
#            'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME22598':[1,1]}



# input for experiment on 11/29/2022
forms=['family_interview_for_genetic_studies_figs','psychs_p1p8','psychs_p9ac32','sofas_screening', 'scid5_schizotypal_personality_sciddpq','scid5_psychosis_mood_substance_abuse']
types=['text', 'radio', 'checkbox', 'dropdown', 'yesno', 'calc']

json_event={'Pronet/PHOENIX/PROTECTED/PronetYA/raw/YA01508/surveys/YA01508.Pronet.json':
            ['screening_arm_1','screening_arm_1','screening_arm_1','screening_arm_1','screening_arm_1','baseline_arm_1'],
            'Pronet/PHOENIX/PROTECTED/PronetPI/raw/PI01355/surveys/PI01355.Pronet.json':
            ['screening_arm_2','screening_arm_2','screening_arm_2','screening_arm_2','screening_arm_2','baseline_arm_2'],
            'Pronet/PHOENIX/PROTECTED/PronetWU/raw/WU05257/surveys/WU05257.Pronet.json':
            ['screening_arm_1','screening_arm_1','screening_arm_1','screening_arm_1','screening_arm_1','baseline_arm_1']}

rpms_dirs={'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME21922':[1,1,1,1,1,2],
           'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME78581':[1,1,1,1,1,2],
           'Prescient/PHOENIX/PROTECTED/PrescientME/raw/ME22598':[1,1,1,1,1,2]}




dfv=pd.DataFrame(columns=['variable','type','subject','value'])

dirbak=getcwd()
chdir('/data/predict/data_from_nda/')

# input section ==================================================================


# PRONET

i=0
for j,form in enumerate(forms):
    
    print(form)
    dfg= groups.get_group(form)
    
    dfg.set_index(var_col, inplace=True)
    
    for v,row in dfg.iterrows():
        # skip the main variable in checkbox
        # only use the expanded ones
        if row[type_col]=='checkbox' and '___' not in v:
            continue

        if row[type_col] in types:
        
            # load json
            for s in json_event.keys():
                
                with open(s) as f:
                    dict1=json.load(f)
            
                for d in dict1:
                
                    # go to screening event
                    if d['redcap_event_name']==json_event[s][j]:
                        
                        # extract value
                        try:
                            dfv.loc[i]= [v, row[type_col], s.split('/')[-1].split('.Pronet.json')[0], d[v]]
                            i+=1
                        except KeyError:
                            pass
                    


print(dfv.shape)


# RPMS


for j,form in enumerate(forms):
    
    print(form)
    dfg= groups.get_group(form)
    
    dfg.set_index(var_col, inplace=True)
    
    for v,row in dfg.iterrows():

        # skip the main variable in checkbox
        # only use the expanded ones
        if row[type_col]=='checkbox' and '___' not in v:
            continue

        if row[type_col] in types:
        
            # load csv
            for d in rpms_dirs.keys():
                
                try:                
                    dfsub=pd.read_csv(glob(f'{d}/surveys/*{form}.csv')[0])
                except IndexError:
                    # the form does not exist for this subject
                    continue
                
                for _,subrow in dfsub.iterrows():
                
                    # go to screening event
                    if int(subrow['visit'])==rpms_dirs[d][j]:
                        
                        # extract value
                        try:
                            dfv.loc[i]= [v, row[type_col], d.split('/')[-1], subrow[v]]
                            i+=1
                        except KeyError:
                            pass
                    


dfv.to_csv(pjoin(sys.argv[2],'redcap_rpms_extracts.csv'),index=False)


chdir(dirbak)


