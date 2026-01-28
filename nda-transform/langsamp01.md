### Steps to prepare data for NDA


1. Obtain a network and event combined `features.csv` file from Phil:

> head -n 3 /path/to/features.csv

```python
...,src_subject_id,interview_type,redcap_event_name,...
...,BM12345,open,baseline_arm_2,...
...,BM23456,open,baseline_arm_1,...
...,BM34567,open,month_2_arm_1,...
```


2. Dheshan filters the above according to following Criteria:

* i. [Interview date](https://github.com/AMP-SCZ/utility/blob/5b530838ca4542e62dca42a784e41e6b11812961/nda-transform/langsamp01.py#L68) in REDCap run sheet must be valid.

* ii. `|expected_interview_date-redcap_interview_date|<=14`

  We could choose `<=30` but that would be too loose.

* iii. Keep only up to a certain event worth of rows. For example, in release-2, we need upto month_2 only.



3. Use a grand script to generate, validate, and submit REDCap data:

```
/data/predict1/utility/nda-transform/_langsamp01.sh open /path/to/features.csv
/data/predict1/utility/nda-transform/_langsamp01.sh psychs /path/to/features.csv
```


4. Prepare features data separately:


#### Post-processing

```
for i in `filtered_features_{open,psychs,diary}.csv.dm1447`; do /data/predict1/utility/nda-transform/langsamp01_post_process.py $i; done
```


#### Preparation

```
for t in open psychs diary
do
    /data/predict1/utility/nda-transform/image03.py --shared ndar_subject01.csv -o langsamp01_features_${t}.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --data /data/predict1/data_from_nda/Language_NDA/scripts/filtered*${t}*.csv --dict langsamp01
done
```

