### Steps to prepare data for NDA

1. Obtain 

Obtain `AMPSCZ_actigraphy_raw_nda.csv`, `AMPSCZ_actigraphy_derived_nda.csv` from Habib Rahimi
in the following format:

```python
$ head -n 3 AMPSCZ_actigraphy_raw_nda.csv
src_subject_id,interview_date,model,start_date,act_start_time,end_date,end_time,time_zone,data_file1_type,data_file1
BI12345,3/31/2023,Axivity Ax3,3/31/2023,17:09,4/25/2023,10:59,EST,parquet,/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/PronetBI/processed/BI12345/actigraphy/mtl_nda/BI-BI12345-actigraphy_Axivity_79925_2023-3-31-17:9-to-2023-4-25-10:59.parquet
BI12345,3/31/2023,Axivity Ax3,3/31/2023,17:09,4/25/2023,10:59,EST,parquet,/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/PronetBI/processed/BI12345/actigraphy/mtl_nda/BI-BI12345-actigraphy_Axivity_79925_2023-3-31-17:9-to-2023-4-25-10:59.parquet
```

The `data_file1` paths can be relative too e.g. `BI12345/actigraphy/mtl_nda/BI-BI12345-actigraphy_Axivity_79925_2023-3-31-17`.

```python
head -n 3 AMPSCZ_actigraphy_derived_nda_revised.csv
subjectkey,src_subject_id,sex,interview_date,interview_age,site_time_zone,UTC_offset,dc_start_date,dc_start_time,dc_end_date,dc_end_time,device,data_modality,temporal_resolution,processing_software,data_file1
,BI02450,,3/31/2023,,America/New_York,-5,3/30/2023,18:00,5/29/2023,18:00,watch,actigraphy,daily,DPSleep,BI02450/actigraphy/mtl_nda/BI-BI02450-actigraphy_sleep_daily_2023-3-31-to-2023-5-29_day26to85.csv
,BI02450,,3/31/2023,,America/New_York,-5,3/30/2023,18:00,5/29/2023,18:00,watch,actigraphy,minute-level,DPSleep,BI02450/actigraphy/mtl_nda/BI-BI02450-actigraphy_scoressleep_2023-3-31-to-2023-5-29_day26to85.csv
```


2. Modify

If `data_file1` is given with absolute path, open the csv in `vim` and run these character replacements:

```
%s+/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/Pronet../processed/++g
%s+/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/Prescient../processed/++g
```

Now you will have relative path. The latter is necessary for organization in collaboration space.


3. Generate

* actirec01

```
cd /data/predict1/to_nda/nda-submissions/network_combined/
/data/predict1/utility/nda-transform/image03.py --shared ndar_subject01.csv -o actirec01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --data ../actirec01/AMPSCZ_actigraphy_raw_nda.csv --dict actirec01
```

* device01

```
/data/predict1/utility/nda-transform/image03.py --shared ndar_subject01.csv -o device01_actirec01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --data ../actirec01/AMPSCZ_actigraphy_derived_nda.csv --dict device01
```

4. Validate

```
vtcmd /data/predict1/to_nda/nda-submissions/network_combined/actirec01.csv
vtcmd /data/predict1/to_nda/nda-submissions/network_combined/device01_actirec01.csv
```

