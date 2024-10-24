# PREDICT cron jobs are distributed among servers to optimally use their bandwidth & loading
# log in to each server and type crontab -e to view/edit them



# === hna002 ===

# generate difference between AMP-SCZ and network data dictionaries
0 6 * * * /data/predict1/utility/_gen_dict_diff.sh 123456 123456 123456 tbillah sbouix gjacobs1



# === dn018 ===

# PRESCIENT real
# determine if new and upload to REDCap
0 18 * * 0,2,4 /data/predict1/miniconda3/bin/python /data/predict1/utility/set_rpms_date_shifts.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ "*/raw/*/surveys/" && /data/predict1/utility/_rpms_to_redcap.sh /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED /data/predict1/utility/rpms-to-yale 123456

# keep six hours difference between upload and download so upload can complete

# clean old arms, download JSONs from REDCap and shift their dates
0 2 * * 1,3,5 /data/predict1/utility/clean_down_shift.sh 123456


# ProNET real
# determine if new and shift dates
# determine if new and upload to REDCap
0 18 * * 1,3,5 /data/predict1/utility/_shift_redcap_dates.sh /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED "*/raw/*/surveys/*.Pronet.json" /data/predict1/utility/yale-real/CloneOfYaleRealRecords_DataDictionary_2024-04-16.csv && /data/predict1/utility/_records_to_redcap.sh /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED /data/predict1/utility/yale-real 123456


# mongodb backup
0 8 * * * /data/predict1/utility/backup_mongodb.sh rc-predict


# kill stale processes every Saturday
0 17 * * 6 pkill -u tb571 python


# === dn018 ===

# upload data tracker CSV files to Dropbox
0 4 * * * /data/predict1/utility/data_tracker_dropbox.sh

# track /data/predict1/ size, every monday at 12 am
0 0 * * 1 /data/predict1/utility/track_briefcase_size.sh /data/predict1/ tbillah sbouix jtbaker



# === dn003 ===

# clear REDCap upload logs, every Friday at 5 pm
0 17 * * 5 rm -rf /data/predict1/utility/bsub/*

# clear NDA upload logs every Monday at 12 am
0 0 * * 1 rm -rf /PHShome/tb571/NDA/nda-tools/vtcmd/*/*

# download EEG run sheets
# every morning at 3 am
0 3 * * * /data/predict1/eeg-qc-dash/down_eeg_pdf_rsheet.sh 123456 /data/predict1/data_from_nda/Pronet
# every morning at 4 am
0 4 * * * /data/predict1/eeg-qc-dash/down_eeg_pdf_rsheet.sh 123456 /data/predict1/data_from_nda/Prescient



# === dn020 ===

# copy EEG QC images over to web app VM
0 */6 * * * /data/predict1/utility/rsync_eegqc.sh /data/predict1/data_from_nda/ /data/eegqc/
0 5 * * * /data/predict1/utility/rsync_eegqc.sh /data/predict1/kcho/flow_test/spero/ /opt/data/eegqc-mock/

10 0 * * * /data/predict1/utility/eegqc_auto_scores.sh /data/predict1/data_from_nda/ /data/eegqc/

0 05 * * * /data/predict1/utility/backup_formqc.sh

# === rc-predict-gen ===

# back up EEG QC web app scores
# run as service account
0 3 * * * /opt/eeg-qc-dash/backup_scores.cron /data/eegqc/ /opt/data/eegqc-mock/
0 0 * * * rsync -a /data/eegqc/.scores.pkl eris2n4.research.partners.org:/data/predict1/data_from_nda/



# === rc-predict ===

# track / size, every day at 12 am
0 0 * * * /opt/track_briefcase_size.sh / tbillah sbouix jtbaker

# generate list of DPdash users
# run as root
0 8 * * * /opt/dpdash/dpdash/get_dpdash_accounts.sh tbillah kchin11 aasgaritarghi tkapur



# === 1200941-Prescient.orygen.org.au ===

SHELL=/bin/bash
HOSTNAME=1200941-Prescient.orygen.org.au

MAILTO=xyz@bwh.harvard.edu
03 20 * * * /mnt/prescient/utility/rpms_cron.sh



# this block was planned but never materialized
# /data/predict1/ backups
# directory,server,frequency (days)

# *,dn025,90
0 19 * */3 THU /data/predict1/utility/backup_predict1.sh predict1-software

# data_from_nda,dn025,7
0 19 * * */FRI /data/predict1/utility/backup_predict1.sh predict1-prod-data

# data_from_nda_dev,dn026,7
0 19 * * */TUE /data/predict1/utility/backup_predict1.sh predict1-dev-data

# home,dn027,7
0 19 * * */WED /data/predict1/utility/backup_predict1.sh predict1-home

# to_nda,dn025,7
0 19 * * */THU /data/predict1/utility/backup_predict1.sh predict1-sub-data



# === dna007 ===
# disk usage tracker for /data/pnl, pnlx, predict1

00 00 * * * /data/predict1/diskusage-logging/logdf

10 00 * * 5 /data/predict1/diskusage-logging/_manual_finger.sh

00 18 * * 5 /data/predict1/diskusage-logging/weekly.sh



# === dn020 ===
# all dpimport are run by tb571
# TODO run by sf284

# generate files status every day
0 17 * * * /data/predict1/utility/generate_files_status1.sh /data/predict1/data_from_nda/

# transfer combined files status to VM for missing data tracker app
0 18 * * * /data/predict1/utility/rsync_files_status.sh

# import all data to production DPdash in succession

# the goal of a fresh import is to make sure that DPdash counts are accurate by Wednesday 6 am
# fresh import happens over Tuesday night - Wednesday morning
0 18 * * 2 /data/predict1/utility/dpimport_files_status.sh /data/predict1/data_from_nda/ rc-predict 1
0 19 * * 2 /data/predict1/utility/dpimport_avlqc.sh /data/predict1/data_from_nda/ rc-predict 1 > /data/predict1/utility/dpimport_avlqc.log.txt 2>&1
0 21 * * 2 /data/predict1/utility/dpimport_formqc.sh /data/predict1/data_from_nda/ rc-predict 1 > /data/predict1/utility/dpimport_formqc.log.txt 2>&1
0 23 * * 2 /data/predict1/utility/dpimport_digital.sh /data/predict1/data_from_nda/ rc-predict 1
0 01 * * 3 /data/predict1/utility/dpimport_mriqc.sh /data/predict1/data_from_nda/ rc-predict 1
0 03 * * 3 /data/predict1/utility/dpimport_eegqc.sh /data/predict1/data_from_nda/ rc-predict 1

# kill all stale import.py every day
0 17 * * * pkill --signal 9 import.py

# incremental import happens on Friday and Sunday
0 18 * * 5,0 /data/predict1/utility/dpimport_files_status.sh /data/predict1/data_from_nda/ rc-predict
0 19 * * 5,0 /data/predict1/utility/dpimport_avlqc.sh /data/predict1/data_from_nda/ rc-predict > /data/predict1/utility/dpimport_avlqc.log.txt 2>&1
0 21 * * 5,0 /data/predict1/utility/dpimport_formqc.sh /data/predict1/data_from_nda/ rc-predict > /data/predict1/utility/dpimport_formqc.log.txt 2>&1
0 23 * * 6,1 /data/predict1/utility/dpimport_digital.sh /data/predict1/data_from_nda/ rc-predict
0 01 * * 6,1 /data/predict1/utility/dpimport_mriqc.sh /data/predict1/data_from_nda/ rc-predict
0 03 * * 6,1 /data/predict1/utility/dpimport_eegqc.sh /data/predict1/data_from_nda/ rc-predict

# recess is on Wednesday, Thursday, Monday

