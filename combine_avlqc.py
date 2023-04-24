#!/usr/bin/env python

from os.path import join as pjoin, dirname
from os import makedirs
import sys
from glob import glob
import pandas as pd
import numpy as np

def concat_site_csv(data_root,output_root,center_name):
    
    print('Combining',center_name)

    if len(center_name)==2:
        # site level combination
        template="processed/*/interviews/*/*_combinedQCRecords.csv"
    else:
        # network level combination
        template="PHOENIX/GENERAL/*/processed/*/interviews/*/*_combinedQCRecords.csv"
        
    individual_qc_paths = glob(f"{data_root}/{template}")
    if not individual_qc_paths:
        return
    
    individual_qc_dfs = [pd.read_csv(x) for x in individual_qc_paths]
    individual_qc_concat = pd.concat(individual_qc_dfs)
    individual_qc_concat.reset_index(drop=True, inplace=True)
    individual_qc_concat.rename(columns={"day":"true_day_num"},inplace=True)
    # so it will display in order of patient ID and within ID the day number
    # if different order is wanted, it needs to change
    individual_qc_concat.sort_values(by="true_day_num",inplace=True)
    individual_qc_concat.sort_values(by="patient",kind="stable",inplace=True)
    dpdash_cols = ["day","reftime","timeofday","weekday"]
    dpdash_cols.extend(individual_qc_concat.columns)
    individual_qc_concat["day"] = [x+1 for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat["reftime"] = [np.nan for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat["timeofday"] = [np.nan for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat["weekday"] = [np.nan for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat = individual_qc_concat[dpdash_cols]
    
    individual_qc_concat.to_csv(f"{output_root}/combined-{center_name}-avlqc-day1to1.csv", index=False)

    # now doing subject-level CSVs with categorical info for the DPDash chart views (3 assessments - open qc, psychs qc, subject open availability)
    # to make sure this runs only when appropriate, do only for Pronet and for Prescient center_name variables (case insensitive)
    if center_name.lower() == "pronet" or center_name.lower() == "prescient":
        # add a CSV with only open interview records, and include a column with categorical label for the DPDash charts
        open_only = individual_qc_concat.drop(columns=["day"])
        open_only = open_only[open_only["interview_type"]=="open"]
        open_only.dropna(subset=["overall_db","num_inaudible"],how='all',inplace=True) # remove records with only video for these purposes, focus on audio
        open_only.reset_index(drop=True,inplace=True)
        open_only["inaudible_per_word"] = [x/(a + b + c) if not np.isnan(x) else np.nan for x,a,b,c in zip(open_only["num_inaudible"].tolist(),open_only["num_words_S1"].tolist(),open_only["num_words_S2"].tolist(),open_only["num_words_S3"].tolist())]

        # 0 awaiting transcription, 
        # 1 excellent (<1% inaud), 
        # 2 good (<5% inaud), 
        # 3 fair (<20% inaud), 
        # 4 usable (>20% inaud but transcript available), 
        # 5 bad (db < 40 so not sent for transcription)
        # note that interviews missing from audio QC due to SOP violations or other issues will not be reflected here at all! 
        # these counts relate only to interviews that were able to be processed by QC
        open_only["audio_quality_category"] = [0 if np.isnan(x) and y > 40 else 
            (5 if np.isnan(x) else 
            (1 if x < 0.01 else 
            (2 if x < 0.05 else 
            (3 if x < 0.2 else 4)))) for x,y in zip(open_only["inaudible_per_word"].tolist(),open_only["overall_db"].tolist())]

        open_only.insert(0, 'day', [x+1 for x in range(open_only.shape[0])])
        # save the overall version anyway even though for the charts need individual CSVs
        open_only.to_csv(f"{output_root}/combined-{center_name}-open_avlqc-day1to1.csv", index=False) # could be imported as open_avlqc instrument

        # now handle the CSVs that will actually be used for the charts - they need to be saved separately for each subject ID
        # instrument here is open_count
        category_cols = ["day","reftime","timeofday","weekday","subject_id","timepoint","audio_quality_category"] # small subset of columns in these CSVs
        for subject_id in set(open_only["patient"].tolist()):
            cur_df = open_only[open_only["patient"]==subject_id].drop(columns=["day"])
            cur_df["subject_id"] = cur_df["patient"]
            cur_df["timepoint"] = cur_df["true_day_num"] # match column names being used for MRI charts (besides the category variable)
            cur_df["day"] = [x+1 for x in range(cur_df.shape[0])]
            cur_df = cur_df[category_cols]
            # note the day number here will indicate the number of available open sessions, not the actual day numbers
            # (timepoint will have the actual day numbers)
            cur_name = subject_id[:2] + "-" + subject_id + "-" + "open_count" + "-" + "day1to" + str(cur_df.shape[0]) + ".csv"
            # they will be saved in subfolder of main folder on the server
            makedirs(f"{output_root}/open_count",exist_ok=True)
            cur_df.to_csv(f"{output_root}/open_count/{cur_name}",index=False)


        # repeat for psychs
        psychs_only = individual_qc_concat.drop(columns=["day"])
        psychs_only = psychs_only[psychs_only["interview_type"]=="psychs"]
        psychs_only.dropna(subset=["overall_db","num_inaudible"],how='all',inplace=True) # remove records with only video for these purposes, focus on audio
        psychs_only.reset_index(drop=True,inplace=True)
        psychs_only["inaudible_per_word"] = [x/(a + b + c) if not np.isnan(x) else np.nan for x,a,b,c in zip(psychs_only["num_inaudible"].tolist(),psychs_only["num_words_S1"].tolist(),psychs_only["num_words_S2"].tolist(),psychs_only["num_words_S3"].tolist())]
       
        # 0 awaiting transcription, 
        # 1 excellent (<1% inaud), 
        # 2 good (<5% inaud), 
        # 3 fair (<20% inaud), 
        # 4 usable (>20% inaud but transcript available), 
        # 5 bad (db < 40 so not sent for transcription)
        # note that interviews missing from audio QC due to SOP violations or other issues will not be reflected here at all! 
        # these counts relate only to interviews that were able to be processed by QC
        psychs_only["audio_quality_category"] = [0 if np.isnan(x) and y > 40 else 
            (5 if np.isnan(x) else 
            (1 if x < 0.01 else 
            (2 if x < 0.05 else 
            (3 if x < 0.2 else 4)))) for x,y in zip(psychs_only["inaudible_per_word"].tolist(),psychs_only["overall_db"].tolist())]

        psychs_only.insert(0, 'day', [x+1 for x in range(psychs_only.shape[0])])
        # save the overall version anyway even though for the charts need individual CSVs
        psychs_only.to_csv(f"{output_root}/combined-{center_name}-psychs_avlqc-day1to1.csv", index=False) # could be imported as psychs_avlqc instrument

        # now handle the CSVs that will actually be used for the charts - they need to be saved separately for each subject ID
        # instrument here is psychs_count
        category_cols = ["day","reftime","timeofday","weekday","subject_id","timepoint","audio_quality_category"] # small subset of columns in these CSVs
        for subject_id in set(psychs_only["patient"].tolist()):
            cur_df = psychs_only[psychs_only["patient"]==subject_id].drop(columns=["day"])
            cur_df["subject_id"] = cur_df["patient"]
            cur_df["timepoint"] = cur_df["true_day_num"] # match column names being used for MRI charts (besides the category variable)
            cur_df["day"] = [x+1 for x in range(cur_df.shape[0])]
            cur_df = cur_df[category_cols]
            # note the day number here will indicate the number of available psychs sessions, not the actual day numbers
            # (timepoint will have the actual day numbers)
            cur_name = subject_id[:2] + "-" + subject_id + "-" + "psychs_count" + "-" + "day1to" + str(cur_df.shape[0]) + ".csv"
            # they will be saved in subfolder of main folder on the server
            makedirs(f"{output_root}/psychs_count",exist_ok=True)
            cur_df.to_csv(f"{output_root}/psychs_count/{cur_name}",index=False)


        # finally, do the open interview availability category by subject ID
        # assessment will be subject_count and variable will be open_transcript_timepoints_category
        # categories are 0 for none, 1 for baseline only, 2 for 2 month only, 3 for both
        # of course this will not distinguish between different types of missingness that have different levels of severity
        trans_avail_df = individual_qc_concat.dropna(subset=["num_inaudible"]) # focusing on transcript availability here!
        for subject_id in set(individual_qc_concat["patient"].tolist()):
            # each CSV will have a single row because now the category is per subject ID
            cur_df = pd.DataFrame()
            cur_df["day"] = [1]
            cur_df["reftime"] = [np.nan]
            cur_df["timeofday"] = [np.nan]
            cur_df["weekday"] = [np.nan]
            cur_df["subject_id"] = [subject_id]
            # now estimate the category. for the time being will require space of at least 40 days to count as two timepoints, and will look for baseline within first 40 days
            check_df = trans_avail_df[trans_avail_df["patient"]==subject_id]
            if check_df.shape[0] == 0:
                cur_df["open_transcript_timepoints_category"] = [0]
            elif check_df.shape[0] == 1:
                if check_df["true_day_num"].tolist()[0] <= 40:
                    cur_df["open_transcript_timepoints_category"] = [1]
                else: # if only transcript is from past study day 40, assume it is a 2 month
                    cur_df["open_transcript_timepoints_category"] = [2]
            else: 
                # handle the mistaken edge cases with more than 2 interviews as if they were real for now, so make this general
                check_days = check_df["true_day_num"].tolist()
                check_days.sort()
                if check_days[0] <= 40:
                    baseline_val = 1
                else:
                    baseline_val = 0
                if check_days[-1] - check_days[0] >= 40:
                    follow_val = 2
                else:
                    follow_val = 0
                cur_df["open_transcript_timepoints_category"] = [baseline_val + follow_val]
                # note details of this category estimation may change later
            cur_name = subject_id[:2] + "-" + subject_id + "-" + "subject_count" + "-" + "day1to1.csv"
            # they will be saved in subfolder of main folder on the server
            makedirs(f"{output_root}/subject_count",exist_ok=True)
            cur_df.to_csv(f"{output_root}/subject_count/{cur_name}",index=False)
    

if __name__ == '__main__':

    concat_site_csv(f'{sys.argv[1]}/Pronet', f'{sys.argv[1]}/AVL_quick_qc', 'PRONET')
    for site in glob(f'{sys.argv[1]}/Pronet/PHOENIX/GENERAL/*'):
        concat_site_csv(site, f'{sys.argv[1]}/AVL_quick_qc', site[-2:])
    
    concat_site_csv(f'{sys.argv[1]}/Prescient', f'{sys.argv[1]}/AVL_quick_qc', 'PRESCIENT')
    for site in glob(f'{sys.argv[1]}/Prescient/PHOENIX/GENERAL/*'):
        concat_site_csv(site, f'{sys.argv[1]}/AVL_quick_qc', site[-2:])

    
