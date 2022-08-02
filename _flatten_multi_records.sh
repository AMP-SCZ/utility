#!/bin/bash

export PATH=/data/predict/miniconda3/bin/:/data/predict/utility/:$PATH

# this script is run from each surveys directory
# ${1} is the subject ID passed as an arg to this script



# unique visit, single file
flatten_multi_records.py ${1}_past_pharmaceutical_treatment.csv

# unique visit, multiple files
flatten_multi_records.py ${1}_family_interview_for_genetic_studies_figs.csv ${1}_family_interview_for_genetic_studies_figs_child.csv ${1}_family_interview_for_genetic_studies_figs_sibling.csv

flatten_multi_records.py ${1}_traumatic_brain_injury_screen.csv ${1}_traumatic_brain_injury_screen_parent.csv ${1}_traumatic_brain_injury_screen_subject.csv



# non-unique visit, single file
flatten_multi_records_1.py ${1}_current_pharmaceutical_treatment_floating_med_125.csv
flatten_multi_records_1.py ${1}_current_pharmaceutical_treatment_floating_med_2650.csv
flatten_multi_records.py ${1}_psychosocial_treatment_form.csv
flatten_multi_records.py ${1}_adverse_events.csv
flatten_multi_records.py ${1}_resource_use_log.csv
flatten_multi_records.py ${1}_health_conditions_medical_historypsychiatric_histo.csv

# non-unique visit, multiple files
flatten_multi_records_1.py ${1}_blood_sample_preanalytic_quality_assurance.csv ${1}_blood_sample_preanalytic_quality_assurance_bc.csv ${1}_blood_sample_preanalytic_quality_assurance_pl.csv ${1}_blood_sample_preanalytic_quality_assurance_se.csv ${1}_blood_sample_preanalytic_quality_assurance_wb.csv

