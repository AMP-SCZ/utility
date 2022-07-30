#!/usr/bin/env python

import pandas as pd
import sys
import re




multi_records= {'adverse_events': {'visit': 99, 'vars': ['chrae_aescreen', 'chrae_?', 'chrae_tp?', 'chrae_diag?', 'chrae_ae?', 'chrae_aes?date', 'chrae_aes?off', 'chr_ae?date', 'chrae_sig?', 'chrae_dr?', 'chrae_d?', 'chrae_e?', 'chrae_expected?', 'chrae_sae?', 'chrae_ssi?', 'chr_ae?date_dr', 'chrae_sig?_dr', 'chrae_ae?_trans_q', 'chrae_ae?_mo?', 'chrae_ae?_mo2', 'chrae_ae?_mo3', 'chrae_ae?_mo4', 'chrae_ae?_mo5', 'chrae_ae?_mo6', 'chrae_ae?_mo7', 'chrae_ae?_mo8', 'chrae_ae?_mo9', 'chrae_ae?_mo10', 'chrae_ae?_mo11', 'chrae_ae?_mo12', 'chrae_ae?_mo18', 'chrae_ae?_mo24', 'chrae_ae?_trans', 'chrae_ae?_offmes', 'chrae_ae?_comments','chrae_add?']},

'psychosocial_treatment_form': {'visit': 99, 'vars': ['chrpsychsoc_concerns', 'chrpsychsoc_treat?', 'chrpsychsoc_treat?_tp', 'chrpsychsoc_treat?_type', 'chrpsychsoc_treat?_other', 'chrpsychsoc_treat?_res', 'chrpsychsoc_treat?_freq', 'chrpsychsoc_treat?_onset', 'chrpsychsoc_treat?_offset', 'chrpsychsoc_treat?_instruct', 'chrpsychsoc_treat?_instruct_other', 'chrpsychsoc_treat?_trans_q', 'chrpsychsoc_treat?_mo1', 'chrpsychsoc_treat?_mo2', 'chrpsychsoc_treat?_mo3', 'chrpsychsoc_treat?_mo4', 'chrpsychsoc_treat?_mo5', 'chrpsychsoc_treat?_mo6', 'chrpsychsoc_treat?_mo7', 'chrpsychsoc_treat?_mo8', 'chrpsychsoc_treat?_mo9', 'chrpsychsoc_treat?_mo10', 'chrpsychsoc_treat?_mo11', 'chrpsychsoc_treat?_mo12', 'chrpsychsoc_treat?_mo18', 'chrpsychsoc_treat?_mo24', 'chrpsychsoc_treat?_trans', 'chrpsychsoc_treat?_offmes', 'chrpsychsoc_treat?_comments','chrpsychsoc_treat?_add']},

'health_conditions_medical_historypsychiatric_histo': {'visit': 99, 'vars': ['chrmed_any', 'chrmed_cond?', 'chrmed_cond?_tp', 'chrmed_cond?_name', 'chrmed_cond?_onset', 'chrcond?_offset', 'chrmed_cond?_instruct', 'chrmed_cond?_trans_q', 'chrmed_cond?_mo1', 'chrmed_cond?_mo2', 'chrmed_cond?_mo3', 'chrmed_cond?_mo4', 'chrmed_cond?_mo5', 'chrmed_cond?_mo6', 'chrmed_cond?_mo7', 'chrmed_cond?_mo8', 'chrmed_cond?_mo9', 'chrmed_cond?_mo10', 'chrmed_cond?_mo11', 'chrmed_cond?_mo12', 'chrmed_cond?_mo18', 'chrmed_cond?_mo24', 'chrmed_cond?_trans', 'chrmed_cond?_offmes', 'chrmed_cond?_comments','chrmed_cond?_add']},

'resource_use_log': {'visit': 99, 'vars': ['chrrul_any', 'chrrul_resource?', 'chrrul_resource?_tp', 'chrrul_resource?_code', 'chrrul_resource?_on', 'chrrul_resource?_off', 'chrrul_resource?_notes','chrrul_resource?_add']},

'traumatic_brain_injury_screen_subject': {'visit': 1, 'vars': ['chrtbi_subject_age?', 'chrtbi_subject_circumstance?', 'chrtbi_subject_length?', 'chrtbi_subject_anterograde?', 'chrtbi_subject_retrograde?', 'chrtbi_subject_symptoms2_?', 'chrtbi_subject_symptom_length?', 'chrtbi_subject_med_find?']},
'traumatic_brain_injury_screen_parent': {'visit': 1, 'vars': ['chrtbi_parent_age?', 'chrtbi_parent_circumstance?', 'chrtbi_parent_length?', 'chrtbi_parent_anterograde?', 'chrtbi_parent_retrograde?', 'chrtbi_parent_symptoms2_?', 'chrtbi_parent_symptom_length?', 'chrtbi_parent_medical_findings?']},

'blood_sample_preanalytic_quality_assurance_bc': {'visit': [2,3], 'vars': ['chrblood_bc?id','chrblood_bc?vol','chrblood_bc?pos','chrblood_bc?box','chrblood_bcfrztime']},
'blood_sample_preanalytic_quality_assurance_pl': {'visit': [2,3], 'vars': ['chrblood_pl?id','chrblood_pl?vol','chrblood_pl?pos','chrblood_pl?hem','chrblood_plfrztime']},
'blood_sample_preanalytic_quality_assurance_wb': {'visit': [2,3], 'vars': ['chrblood_wb?id','chrblood_wb?vol','chrblood_wb?pos','chrblood_wbfrztime']},
'blood_sample_preanalytic_quality_assurance_se': {'visit': [2,3], 'vars': ['chrblood_se?id','chrblood_se?vol','chrblood_se?pos','chrblood_serumfrztime','chrblood_sehem','chrblood_selip']},

'family_interview_for_genetic_studies_figs_child': {'visit': 1, 'vars': ['chrfigs_child?_age','chrfigs_child?_sex','chrfigs_child?_info','chrfigs_child?_s01','chrfigs_child?_s02','chrfigs_child?_s03','chrfigs_child?_s04','chrfigs_child?_s05','chrfigs_child?_s06','chrfigs_child?_s07','chrfigs_child?_s08','chrfigs_child?_d01','chrfigs_child?_d02','chrfigs_child?_d03','chrfigs_child?_d04','chrfigs_child?_d05','chrfigs_child?_d06','chrfigs_child?_d07','chrfigs_child?_d08','chrfigs_child?_d10','chrfigs_child?_d11','chrfigs_child?_d12','chrfigs_child?_m01','chrfigs_child?_m02','chrfigs_child?_m03','chrfigs_child?_m04','chrfigs_child?_m05','chrfigs_child?_m06','chrfigs_child?_m07','chrfigs_child?_m08','chrfigs_child?_m09','chrfigs_child?_m10','chrfigs_child?_m11','chrfigs_child?_m12','chrfigs_child?_p01','chrfigs_child?_p02','chrfigs_child?_p03','chrfigs_child?_p04','chrfigs_child?_p05','chrfigs_child?_p06','chrfigs_child?_p07','chrfigs_child?_p08','chrfigs_child?_p09','chrfigs_child?_p10','chrfigs_child?_p11','chrfigs_child?_p12','chrfigs_child?_p13','chrfigs_child?_p14','chrfigs_child?_p15','chrfigs_child?_p16','chrfigs_child?_p17','chrfigs_child?_p18']},
'family_interview_for_genetic_studies_figs_sibling': {'visit': 1, 'vars': ['chrfigs_sibling?_age','chrfigs_sibling?_sex','chrfigs_sibling?_info','chrfigs_sibling?_s01','chrfigs_sibling?_s02','chrfigs_sibling?_s03','chrfigs_sibling?_s04','chrfigs_sibling?_s05','chrfigs_sibling?_s06','chrfigs_sibling?_s07','chrfigs_sibling?_s08','chrfigs_sibling?_d01','chrfigs_sibling?_d02','chrfigs_sibling?_d03','chrfigs_sibling?_d04','chrfigs_sibling?_d05','chrfigs_sibling?_d06','chrfigs_sibling?_d07','chrfigs_sibling?_d08','chrfigs_sibling?_d10','chrfigs_sibling?_d11','chrfigs_sibling?_d12','chrfigs_sibling?_m01','chrfigs_sibling?_m02','chrfigs_sibling?_m03','chrfigs_sibling?_m04','chrfigs_sibling?_m05','chrfigs_sibling?_m06','chrfigs_sibling?_m07','chrfigs_sibling?_m08','chrfigs_sibling?_m09','chrfigs_sibling?_m10','chrfigs_sibling?_m11','chrfigs_sibling?_m12','chrfigs_sibling?_p01','chrfigs_sibling?_p02','chrfigs_sibling?_p03','chrfigs_sibling?_p04','chrfigs_sibling?_p05','chrfigs_sibling?_p06','chrfigs_sibling?_p07','chrfigs_sibling?_p08','chrfigs_sibling?_p09','chrfigs_sibling?_p10','chrfigs_sibling?_p11','chrfigs_sibling?_p12','chrfigs_sibling?_p13','chrfigs_sibling?_p14','chrfigs_sibling?_p15','chrfigs_sibling?_p16','chrfigs_sibling?_p17','chrfigs_sibling?_p18']},

'current_pharmaceutical_treatment_floating_med_125': {'visit': 99, 'vars': ['chrpharm_med','chrpharm_med?_comments','chrpharm_med?_name','chrpharm_dose_lowerlimit_med?','chrpharm_dose_upperlimit_med?','chrpharm_med?_onset','chrpharm_med?_offset','chrpharm_med?_use','chrpharm_med?_dosage','chrpharm_med?_frequency','chrpharm_med?_datasource','chrpharm_med?_other','chrpharm_med?_comp','chrpharm_med?_indication','chrpharm_med?_other2','chrpharm_firstdose_med?','chrpharm_med?_add']},

'current_pharmaceutical_treatment_floating_med_2650': {'visit': 99, 'vars': ['chrpharm_med_past','chrpharm_med?_comments','chrpharm_med?_name','chrpharm_dose_lowerlimit_med?','chrpharm_dose_upperlimit_med?','chrpharm_med?_onset','chrpharm_med?_offset','chrpharm_med?_use','chrpharm_med?_dosage','chrpharm_med?_frequency','chrpharm_med?_datasource','chrpharm_med?_other','chrpharm_med?_comp','chrpharm_med?_indication','chrpharm_med?_other2','chrpharm_firstdose_med?','chrpharm_med?_add_past']},

'past_pharmaceutical_treatment': {'visit': 1, 'vars': ['chrpharm_med?_comments_past','chrpharm_med?_name_past','chrpharm_dose_lowerlimit_med?_past','chrpharm_dose_upperlimit_med?_past','chrpharm_med?_onset_past','chrpharm_med?_offset_past','chrpharm_med?_use_past','chrpharm_med?_dosage_past','chrpharm_med?_frequency_past','chrpharm_med?_datasource_past','chrpharm_med?_other_past','chrpharm_med?_comp_past','chrpharm_med1_indication_past','chrpharm_med?_other2_past']},

}

def flatten_one(filename):

    subjectkey= filename.split('_')[0]
    form= re.search(f'{subjectkey}_(.+?).csv', filename).group(1)

    df= pd.read_csv(filename)
    cols= df.columns[5:-1]


    # new single-row data frame with default columns
    df1= df.loc[:0][df.columns[:5]]

    dict1={}
    dict1['visit']= df.loc[0,'visit'] if 'visit' in df else multi_records[form]['visit']
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

    return df1


def flatten_many():

    df1= pd.read_csv(sys.argv[1])
    for filename in sys.argv[2:]:
        df= flatten_one(filename)
        df1= pd.concat([df1,df[df.columns[6:]]],axis=1)

    return df1
    


def flatten_group(df,form,cols):

    dict1={}
    dict1['visit']= df.loc[0,'visit'] if 'visit' in df else multi_records[form]['visit']
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

    return dict1


def flatten_one_new(filename):

    dfmulti= pd.read_csv(filename)

    subjectkey= filename.split('_')[0]
    form= re.search(f'{subjectkey}_(.+?).csv', filename).group(1)

    default_cols= ['LastModifiedDate','subjectkey','interview_date','interview_age','gender']
    cols= [c for c in dfmulti.columns if c not in default_cols]

    dfall= pd.DataFrame()
    groups= dfmulti.groupby('visit')
    for timepoint in groups.groups.keys():
            
        dfvisit= groups.get_group(timepoint).reset_index()
        
        # new single-row data frame with default columns for that timepoint/visit
        df1= dfvisit.loc[:0][default_cols]
        dict1= flatten_group(dfvisit,form,cols)
        
        # vertically concatenate default columns and flat list
        df1= pd.concat([df1,pd.DataFrame([dict1])], axis=1)

        # horizontally concatenate flat lists
        dfall= pd.concat([dfall,df1], axis=0, sort=False)


    return dfall


if __name__=='__main__':

    if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
        print(f'''Usage: {__file__} /path/to/ME57953_multi_record_form.csv
This program transforms a multi-row record into uniquely-named columns for REDCap import.
Observe *.csv.flat output file.''')
        exit(0)


    df2=flatten_one_new(sys.argv[1])

    output= sys.argv[1]+'.flat'
    df2.to_csv(output, index=False)
    print('Generated', output)


