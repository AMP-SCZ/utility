#!/usr/bin/env python

import pandas as pd
import sys
import re


if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {__file__} /path/to/ME57953_multi_record_form.csv
This program transforms a multi-row record into uniquely-named columns for REDCap import.
Observe *.csv.flat output file.''')
    exit(0)

multi_records= {'adverse_events': {'visit': 99, 'vars': ['chrae_aescreen', 'chrae_?', 'chrae_tp?', 'chrae_diag?', 'chrae_ae?', 'chrae_aes?date', 'chrae_aes?off', 'chr_ae?date', 'chrae_sig?', 'chrae_dr?', 'chrae_d?', 'chrae_e?', 'chrae_expected?', 'chrae_sae?', 'chrae_ssi?', 'chr_ae?date_dr', 'chrae_sig?_dr', 'chrae_ae?_trans_q', 'chrae_ae?_mo?', 'chrae_ae?_mo2', 'chrae_ae?_mo3', 'chrae_ae?_mo4', 'chrae_ae?_mo5', 'chrae_ae?_mo6', 'chrae_ae?_mo7', 'chrae_ae?_mo8', 'chrae_ae?_mo9', 'chrae_ae?_mo10', 'chrae_ae?_mo11', 'chrae_ae?_mo12', 'chrae_ae?_mo18', 'chrae_ae?_mo24', 'chrae_ae?_trans', 'chrae_ae?_offmes', 'chrae_ae?_comments','chrae_add?']},

'psychosocial_treatment_form': {'visit': 99, 'vars': ['chrpsychsoc_concerns', 'chrpsychsoc_treat?', 'chrpsychsoc_treat?_tp', 'chrpsychsoc_treat?_type', 'chrpsychsoc_treat?_other', 'chrpsychsoc_treat?_res', 'chrpsychsoc_treat?_freq', 'chrpsychsoc_treat?_onset', 'chrpsychsoc_treat?_offset', 'chrpsychsoc_treat?_instruct', 'chrpsychsoc_treat?_instruct_other', 'chrpsychsoc_treat?_trans_q', 'chrpsychsoc_treat?_mo1', 'chrpsychsoc_treat?_mo2', 'chrpsychsoc_treat?_mo3', 'chrpsychsoc_treat?_mo4', 'chrpsychsoc_treat?_mo5', 'chrpsychsoc_treat?_mo6', 'chrpsychsoc_treat?_mo7', 'chrpsychsoc_treat?_mo8', 'chrpsychsoc_treat?_mo9', 'chrpsychsoc_treat?_mo10', 'chrpsychsoc_treat?_mo11', 'chrpsychsoc_treat?_mo12', 'chrpsychsoc_treat?_mo18', 'chrpsychsoc_treat?_mo24', 'chrpsychsoc_treat?_trans', 'chrpsychsoc_treat?_offmes', 'chrpsychsoc_treat?_comments','chrpsychsoc_treat?_add']},

'health_conditions_medical_historypsychiatric_histo': {'visit': 99, 'vars': ['chrmed_any', 'chrmed_cond?', 'chrmed_cond?_tp', 'chrmed_cond?_name', 'chrmed_cond?_onset', 'chrcond?_offset', 'chrmed_cond?_instruct', 'chrmed_cond?_trans_q', 'chrmed_cond?_mo1', 'chrmed_cond?_mo2', 'chrmed_cond?_mo3', 'chrmed_cond?_mo4', 'chrmed_cond?_mo5', 'chrmed_cond?_mo6', 'chrmed_cond?_mo7', 'chrmed_cond?_mo8', 'chrmed_cond?_mo9', 'chrmed_cond?_mo10', 'chrmed_cond?_mo11', 'chrmed_cond?_mo12', 'chrmed_cond?_mo18', 'chrmed_cond?_mo24', 'chrmed_cond?_trans', 'chrmed_cond?_offmes', 'chrmed_cond?_comments','chrmed_cond?_add']},

'resource_use_log': {'visit': 99, 'vars': ['chrrul_any', 'chrrul_resource?', 'chrrul_resource?_tp', 'chrrul_resource?_code', 'chrrul_resource?_on', 'chrrul_resource?_off', 'chrrul_resource?_notes','chrrul_resource?_add']},

'traumatic_brain_injury_screen_subject': {'visit': 1, 'vars': ['chrtbi_subject_age?', 'chrtbi_subject_circumstance?', 'chrtbi_subject_length?', 'chrtbi_subject_anterograde?', 'chrtbi_subject_retrograde?', 'chrtbi_subject_symptoms2_?', 'chrtbi_subject_symptom_length?', 'chrtbi_subject_med_find?']},
'traumatic_brain_injury_screen_parent': {'visit': 1, 'vars': ['chrtbi_parent_age?', 'chrtbi_parent_circumstance?', 'chrtbi_parent_length?', 'chrtbi_parent_anterograde?', 'chrtbi_parent_retrograde?', 'chrtbi_parent_symptoms2_?', 'chrtbi_parent_symptom_length?', 'chrtbi_parent_medical_findings?']},

'blood_sample_preanalytic_quality_assurance_bc': {'visit': [2,3], 'vars': ['chrblood_bc?id','chrblood_bc?vol','chrblood_bc?pos','chrblood_bc?box','chrblood_bcfrztime']},
'blood_sample_preanalytic_quality_assurance_pl': {'visit': [2,3], 'vars': ['chrblood_pl?id','chrblood_pl?vol','chrblood_pl?pos','chrblood_pl?hem','chrblood_plfrztime']},
'blood_sample_preanalytic_quality_assurance_wb': {'visit': [2,3], 'vars': ['chrblood_wb?id','chrblood_wb?vol','chrblood_wb?pos','chrblood_wbfrztime']},
'blood_sample_preanalytic_quality_assurance_se': {'visit': [2,3], 'vars': ['chrblood_se?id','chrblood_se?vol','chrblood_se?pos','chrblood_sefrztime','chrblood_sehem','chrblood_selip']},

}


subjectkey= sys.argv[1].split('_')[0]
form= re.search(f'{subjectkey}_(.+?).csv', sys.argv[1]).group(1)

df= pd.read_csv(sys.argv[1])
cols= df.columns[5:-1]


# new single-row data frame with default columns
df1= df.loc[:0][df.columns[:5]]

dict1={}
dict1['visit']= df['visit'] if 'visit' in df else multi_records[form]['visit']
for v in multi_records[form]['vars']:

    # has the variable been exported by RPMS?
    if v.replace('?','') in cols:
        c= v.replace('?','')
    elif v.replace('_?','') in cols:
        c= v.replace('_?','')
    else:
        continue
        
    # go through the rows of that variable and generate a flat list
    for i,row in df.iterrows():
        dict1[v.replace('?',str(row['Row#']))]= row[c]
        

# for n repeats, there are n-1 *_add vars, so delete the nth *_add var
for v in multi_records[form]['vars']:
    if '_add' in v:
        del dict1[v.replace('?',str(df.shape[0]))]
        break


# concatenate default columns and flat list
df1= pd.concat([df1,pd.DataFrame([dict1])], axis=1)

output= sys.argv[1]+'.flat'
df1.to_csv(output, index=False)
print('Generated', output)


