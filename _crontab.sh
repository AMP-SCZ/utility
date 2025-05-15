# PREDICT cron jobs are distributed among servers to optimally use their bandwidth & loading
# log in to each server and type crontab -e to view/edit them



# === hna002 ===

# generate difference between AMP-SCZ and network data dictionaries
0 6 * * * /data/predict1/utility/_gen_dict_diff.sh 123456 123456 123456 tbillah sbouix dmohandass oborders



# === dn018 ===

# PRESCIENT real
# determine if new and upload to REDCap
0 18 * * 0,2,4 /data/predict1/miniconda3/bin/python /data/predict1/utility/set_rpms_date_shifts.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ "*/raw/*/surveys/" && /data/predict1/utility/_rpms_to_redcap.sh /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED /data/predict1/utility/yale-real 123456

# keep six hours difference between upload and download so upload can complete

# clean old arms, download JSONs from REDCap and shift their dates
0 2 * * 1,3,5 /data/predict1/utility/clean_down_shift.sh 123456


# ProNET real
# determine if new and shift dates
# determine if new and upload to REDCap
0 18 * * 1,3,5 /data/predict1/utility/_shift_redcap_dates.sh /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED "*/raw/*/surveys/*.Pronet.json" /data/predict1/utility/yale-real/*_DataDictionary_*.csv && /data/predict1/utility/_records_to_redcap.sh /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED /data/predict1/utility/yale-real 123456


# mongodb backup
0 8 * * * /data/predict1/utility/backup_mongodb.sh rc-predict


# kill stale processes every Saturday
0 17 * * 6 pkill -u tb571 python


# upload data tracker CSV files to Dropbox
0 4 * * * /data/predict1/utility/data_tracker_dropbox.sh

# track /data/predict1/ size, every monday at 12 am
0 0 * * 1 /data/predict1/utility/track_briefcase_size.sh /data/predict1/ tbillah sbouix jtbaker



# === dna007 ===

# clear REDCap upload logs, every Friday at 5 pm
0 17 * * 5 rm -rf /data/predict1/utility/bsub/*
0 17 * * 5 rm -rf /data/predict1/utility/slurm/*

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
0 8 * * * /opt/dpdash/dpdash/get_dpdash_accounts.sh tbillah kchin11 tkapur



# === 1200941-Prescient.orygen.org.au ===

SHELL=/bin/bash
HOSTNAME=1200941-Prescient.orygen.org.au

MAILTO=xyz@bwh.harvard.edu
03 20 * * * /mnt/prescient/utility/rpms_cron.sh



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
# fresh import happens over Monday night - Tuesday morning
0 18 * * 1 /data/predict1/utility/dpimport_files_status.sh /data/predict1/data_from_nda/ rc-predict 1
0 19 * * 1 /data/predict1/utility/dpimport_avlqc.sh /data/predict1/data_from_nda/ rc-predict 1 > /data/predict1/utility/dpimport_avlqc.log.txt 2>&1
0 21 * * 1 /data/predict1/utility/dpimport_formqc.sh /data/predict1/data_from_nda/ rc-predict 1 > /data/predict1/utility/dpimport_formqc.log.txt 2>&1
0 23 * * 1 /data/predict1/utility/dpimport_digital.sh /data/predict1/data_from_nda/ rc-predict 1
0 01 * * 2 /data/predict1/utility/dpimport_mriqc.sh /data/predict1/data_from_nda/ rc-predict 1
0 03 * * 2 /data/predict1/utility/dpimport_eegqc.sh /data/predict1/data_from_nda/ rc-predict 1


# kill all stale import.py every day
0 17 * * * pkill --signal 9 import.py

# incremental import happens on Thursday and Saturday
0 18 * * 4,6 /data/predict1/utility/dpimport_files_status.sh /data/predict1/data_from_nda/ rc-predict
0 19 * * 4,6 /data/predict1/utility/dpimport_avlqc.sh /data/predict1/data_from_nda/ rc-predict > /data/predict1/utility/dpimport_avlqc.log.txt 2>&1
0 21 * * 4,6 /data/predict1/utility/dpimport_formqc.sh /data/predict1/data_from_nda/ rc-predict > /data/predict1/utility/dpimport_formqc.log.txt 2>&1
0 23 * * 5,0 /data/predict1/utility/dpimport_digital.sh /data/predict1/data_from_nda/ rc-predict
0 01 * * 5,0 /data/predict1/utility/dpimport_mriqc.sh /data/predict1/data_from_nda/ rc-predict
0 03 * * 5,0 /data/predict1/utility/dpimport_eegqc.sh /data/predict1/data_from_nda/ rc-predict

# recess are Tuesday, Wednesday, Friday, Sunday nights

