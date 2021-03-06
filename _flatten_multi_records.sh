#!/bin/bash

export PATH=/data/predict/miniconda3/bin/:/data/predict/utility/:$PATH

# this script is run from each surveys directory
# ${1} is the subject ID passed as an arg to this script


flatten_multi_records.py ${1}_adverse_events.csv
flatten_multi_records.py ${1}_health_conditions_medical_historypsychiatric_histo.csv
flatten_multi_records.py ${1}_psychosocial_treatment_form.csv
flatten_multi_records.py ${1}_resource_use_log.csv


flatten_multi_records.py ${1}_blood_sample_preanalytic_quality_assurance.csv ${1}_blood_sample_preanalytic_quality_assurance_bc.csv ${1}_blood_sample_preanalytic_quality_assurance_pl.csv ${1}_blood_sample_preanalytic_quality_assurance_se.csv ${1}_blood_sample_preanalytic_quality_assurance_wb.csv

flatten_multi_records.py ${1}_family_interview_for_genetic_studies_figs.csv ${1}_family_interview_for_genetic_studies_figs_child.csv ${1}_family_interview_for_genetic_studies_figs_sibling.csv

flatten_multi_records.py ${1}_traumatic_brain_injury_screen.csv ${1}_traumatic_brain_injury_screen_parent.csv ${1}_traumatic_brain_injury_screen_subject.csv


