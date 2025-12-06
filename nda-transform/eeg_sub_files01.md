### Steps to prepare data for NDA


1. Obtain `.csv` files from Spero that are already date shifted. Tashrif may need to insert `experiment_id` 2201.
   It can be done via `vim`. A snippet of one of the CSV files is given below:
   
```
head -n 3 NDArel4_eeg_raw.csv
subjectkey,src_subject_id,interview_date,interview_age,sex,experiment_id,visit,experiment_validity,data_file1,data_file1_type
,BM06276,10/20/2023,,,2201,baseline,4,BM06276/eeg/ses-20231020/BM06276_eeg_visit1.zip,BrainVision Core Data Format 1.0
,BM08191,10/24/2023,,,2201,baseline,4,BM08191/eeg/ses-20231024/BM08191_eeg_visit1.zip,BrainVision Core Data Format 1.0
...
```

2. Populate the mandatory columns in `eeg_sub_files01.py`, `ampscz_eeg_featurestask01` , `ampscz_eeg_featuresrest01`:

```
cd /data/predict1/to_nda/nda-submissions/network_combined/
/data/predict1/utility/nda-transform/eeg_sub_files01.py --dict eeg_sub_files01 --shared ndar_subject01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o eeg_sub_files01.csv --data /data/predict1/data_from_nda/EEGqc_features/NDA/rel04/NDArel4_eeg_raw.csv
/data/predict1/utility/nda-transform/eeg_sub_files01.py --dict eeg_featurestask01 --shared ndar_subject01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o eeg_featurestask01.csv --data /data/predict1/data_from_nda/EEGqc_features/NDA/rel04/NDArel4_eeg_featurestask01.csv 
/data/predict1/utility/nda-transform/eeg_sub_files01.py --dict eeg_featuresrest01 --shared ndar_subject01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o eeg_featuresrest01.csv --data /data/predict1/data_from_nda/EEGqc_features/NDA/rel04/NDArel4_eeg_featuresrest01.csv 
```

3. validate

> vtcmd \*eeg*csv
