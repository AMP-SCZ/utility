### Steps to prepare data for NDA


1. Obtain `.csv` files from Spero that are already date shifted. Tashrif may need to insert `experiment_id` 2201. It can be done via `vim`.



3. Populate the mandatory columns in `eeg_sub_files01.py`, `ampscz_eeg_featurestask01` , `ampscz_eeg_featuresrest01`:

```
cd /data/predict1/to_nda/nda-submissions/network_combined/
/data/predict1/utility/nda-transform/eeg_sub_files01.py --dict eeg_sub_files01 --shared ndar_subject01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o eeg_sub_files01.csv --data /data/predict1/data_from_nda/EEGqc_features/NDA/rel04/NDArel4_eeg_raw.csv
/data/predict1/utility/nda-transform/eeg_sub_files01.py --dict eeg_featurestask01 --shared ndar_subject01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o eeg_featurestask01.csv --data /data/predict1/data_from_nda/EEGqc_features/NDA/rel04/NDArel4_eeg_featurestask01.csv 
/data/predict1/utility/nda-transform/eeg_sub_files01.py --dict eeg_featuresrest01 --shared ndar_subject01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o eeg_featuresrest01.csv --data /data/predict1/data_from_nda/EEGqc_features/NDA/rel04/NDArel4_eeg_featuresrest01.csv 
```

# validate

> vtcmd *eeg*csv
