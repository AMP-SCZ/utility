### Steps to prepare data for NDA

1. Obtain `.txt` file from Spero per visit with one zip file in each line:

> head -n 3 nda-submissions/eeg_sub_files01/AMPSCZ_EEG_NDArel2_baseline.txt

```python
/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/PrescientBM/processed/BM12345/eeg/ses-20231013/NDA/BM12345_eeg_visit001.zip
/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/PrescientBM/processed/BM67890/eeg/ses-20231031/NDA/BM67890_eeg_visit001.zip
```

2. Shift dates and prepare NDA compatible file with empty mandatory columns:

```
/data/predict1/utility/nda-transform/_eeg_sub_files01.py /path/to/AMPSCZ_EEG_baseline.txt
head -n 3 nda-submissions/eeg_sub_files01/AMPSCZ_EEG_NDArel2_baseline.csv
```

```python
subjectkey,src_subject_id,interview_date,interview_age,sex,experiment_id,data_file1,data_file1_type
,BM12345,10/20/2023,,,2201,/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/PrescientBM/processed/BM12345/eeg/ses-20231020/NDA/BM12345_eeg_visit001.zip,
,BM67890,10/24/2023,,,2201,/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/PrescientBM/processed/BM67890/eeg/ses-20231024/NDA/BM67890_eeg_visit001.zip,
```

3. Populate the mandatory columns using `eeg_sub_files01.py` per visit.

```bash
cd /data/predict1/to_nda/nda-submissions/network_combined/
/data/predict1/utility/nda-transform/eeg_sub_files01.py --dict eeg_sub_files01 --shared ndar_subject01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -e baseline --data ../eeg_sub_files01/*csv
```
