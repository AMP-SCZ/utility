### Steps to prepare data for NDA


1. Obtain data from Yoonho Chung as:

> head -n 3 ampscz-n131-phone_sensors-20240308.csv

```python
subjectkey,src_subject_id,sex,interview_date,interview_age,time_zone,UTC_offset,start_date,start_time,end_date,end_time,sample_frequency,data_file1,data_modality,phone_device_type,phone_operatingsystem_versions,phone_application,phone_application_versions,software_preproc
,CA12345,,,,MST,-7,12/05/2022,00:00,12/05/2022,23:59,5,/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/PronetCA/processed/CA12345/phone/mtl_nda/CA-CA12345-phone_gps_2022-12-5_14.parquet,geolocation,iPhone10 5,iOS 16.1.2,MindLAMP,,
,CA12345,,,,MST,-7,12/06/2022,00:00,12/06/2022,23:59,5,/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/PronetCA/processed/CA12345/phone/mtl_nda/CA-CA12345-phone_gps_2022-12-6_15.parquet,geolocation,iPhone10 5,iOS 16.1.2,MindLAMP,,
...
...
```

> head -n 3 ampscz-n195-phone_survey-20240313.csv

```python
subjectkey,src_subject_id,sex,interview_date,interview_age,time_zone,UTC_offset,start_date,start_time,phone_survey_duration,phone_device_type,phone_operatingsystem_versions,phone_application,phone_application_versions,cheerful,cheerful_duration,stressed,stressed_duration,down,down_duration,strange,strange_duration,content,content_duration,suspicious,suspicious_duration,relaxed,relaxed_duration,racing,racing_duration,enthusiastic,enthusiastic_duration,auditory,auditory_duration,empty,empty_duration,anxious,anxious_duration,concentrate,concentrate_duration,irritable,irritable_duration,worried,worried_duration,enjoy,enjoy_duration,mind,mind_duration,lonely,lonely_duration,special,special_duration,energetic,energetic_duration,control,control_duration,motivated,motivated_duration,confused,confused_duration,visual,visual_duration,undertaking,underatking_duration,function,function_duration,socialp,socialp_duration,sociald,sociald_duration,negative,negative_duration,positive,positive_duration
,CA12345,,,,MST,-7,12/05/2022,22:15,,iPhone10 5,iOS 16.1.2,MindLAMP,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,,4,
,CA12345,,,,MST,-7,12/06/2022,04:27,,iPhone10 5,iOS 16.1.2,MindLAMP,,5,,3,,2,,5,,4,,2,,5,,7,,5,,2,,1,,4,,3,,4,,3,,7,,1,,2,,2,,5,,1,,5,,2,,1,,6,,6,,6,,2,,3,,6,
...
...
```


2. Generate NDA compatible data:

* ampscz_sp_sensors01

```bash
cd /data/predict1/to_nda/nda-submissions/network_combined

/data/predict1/utility/nda-transform/ampscz_sp_survey01.py -o ampscz_sp_survey01.csv --root /data/predict1/data_from_nda/ -t "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --shared ndar_subject01.csv --dict ampscz_sp_survey01 --data ../mindlamp/*-phone_survey-20240308.csv --interview_date_var start_date

/data/predict1/utility/nda-transform/ampscz_sp_sensors01.py -o ampscz_sp_sensors01.csv --root /data/predict1/data_from_nda/ -t "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --shared ndar_subject01.csv --dict ampscz_sp_sensors01 --data ../mindlamp/*-phone_sensors-20240308.csv --interview_date_var start_date

/data/predict1/utility/nda-transform/_ampscz_sp_sensors01.sh ampscz_sp_sensors01.csv

```

* device01

```
/data/predict1/utility/nda-transform/image03.py --shared ndar_subject01.csv -o device01_ampscz_sp_sensors01.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --data ../mindlamp/*-derived_sensors-20241113.csv --dict device01
```

3. Validate as:

> python /data/predict1/nda-tools/NDATools/clientscripts/vtcmd.py /data/predict1/to_nda/nda-submissions/network_combined/ampscz_sp_sensors01.csv

> python /data/predict1/nda-tools/NDATools/clientscripts/vtcmd.py /data/predict1/to_nda/nda-submissions/network_combined/ampscz_sp_survey01.csv

> python /data/predict1/nda-tools/NDATools/clientscripts/vtcmd.py /data/predict1/to_nda/nda-submissions/network_combined/device01_ampscz_sp_sensors01.csv


4. Submit as:

```bash
cd /data/predict1/utility/nda-transform/
./submit.sh -f ampscz_sp_sensors01 -e 3705 -u tbillah
./submit.sh -f ampscz_sp_sensors01 -e 4366 -c 4366 -u tbillah
./submit.sh -f ampscz_sp_survey01 -u tbillah
```
