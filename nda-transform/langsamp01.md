### Steps to prepare data for NDA


1. Obtain network and event combined `.csv` file from Phil and Dheshan per `interview_type`:

> head -n 3 nda-bmissions/langsamp01/AMPSCZ_open_20240227.csv

*(Notice where the string `open` exists in its name)*

```python
study,subject,interview_type,day,interview_number,expected_interview_date,closest_interview_date,redcap_event_name
PrescientBM,BM12345,open,20,1,2023-10-31,2023-10-31,baseline_arm_2
PrescientBM,BM23456,open,50,1,2023-11-14,2023-11-14,baseline_arm_1
PrescientBM,BM34567,open,119,2,2024-01-22,2024-01-22,month_2_arm_1
```

Criteria for populating rows in the above csv:

* i. `|expected_interview_date-closest_interview_date|<=14`

We could choose `<=30` but that would be too loose.

* ii. Keep only up to a certain event worth of rows. For example, in release-2, we need upto month_2 only.


2. Use the grand script to generate, validate, and submit its data:

```
/data/predict1/utility/nda-transform/_langsamp01.sh open 20240227.csv
/data/predict1/utility/nda-transform/_langsamp01.sh psychs 20240227.csv
```

The `langsamp01.py` filters the candidate csv provided in #1 as follows:

* i. Redacted transcript with `+day` or `-day` and `interview_number` must exist in disk.

* ii. A row with `+day` or `-day` and `interview_number` must exist in combined QC records.

* iii. Interview day in REDCap run sheet must be valid.

* iv. All NDA mandatory variables must exist for that subject.

If any of the above four are not met, that candidate cannot be uploaded to NDA and is omitted.

