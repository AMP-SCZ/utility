### Steps to prepare data for NDA

1. Obtain 

Obtain `Pronet_Axivity_nda_20240221.csv`, `Prescient_Axivity_nda_20240221.csv` from Habib Rahimi
in the following format:

```python
$ head -n 5 Pronet_Axivity_nda_20240221.csv
src_subject_id,interview_date,model,start_date,act_start_time,end_date,end_time,time_zone,data_file1_type,data_file1
BI12345,3/31/2023,Axivity Ax3,3/31/2023,17:09,4/25/2023,10:59,EST,parquet,BI12345/actigraphy/mtl_nda/BI-BI12345-actigraphy_Axivity_79925_2023-3-31-17:9-to-2023-4-25-10:59.parquet
BI12345,3/31/2023,Axivity Ax3,3/31/2023,17:09,4/25/2023,10:59,EST,parquet,BI12345/actigraphy/mtl_nda/BI-BI12345-actigraphy_Axivity_79925_2023-3-31-17:9-to-2023-4-25-10:59.parquet
```


2. Modify

i. Concatenate to one file:

```
cd /data/predict1/to_nda/nda-submissions/actirec01
cp Pronet_Axivity_nda_20240221.csv actirec01_20240221.csv
tail -n +2 Prescient_Axivity_nda_20240221.csv >> actirec01_20240221.csv
```

ii. Introduce line break after Pronet entities in Vim.

iii. Prepend three empty columns:

> subjectkey,interview_age,sex,


3. Generate

```
cd /data/predict1/to_nda/nda-submissions/network_combined/
python -m pdb /data/predict1/utility/nda-transform/image03.py --shared ndar_subject01.csv -o actirec01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --data ../actirec01/actirec01_20240221.csv --dict actirec01
```

4. Validate

> python /data/predict1/nda-tools/NDATools/clientscripts/vtcmd.py /data/predict1/to_nda/nda-submissions/network_combined/actirec01.csv


