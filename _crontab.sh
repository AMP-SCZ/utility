# PREDICT cron jobs are distributed among servers to optimally use their bandwidth & loading
# log in to each server and type crontab -e to view/edit them



# === hna002 ===

# generate lochness datalake's files status at 6 am and 9pm for dpdash
30 6,21 * * * * /data/predict1/utility/generate_files_status.sh /data/predict1/data_from_nda_dev/ dpstage

# import AVL QC data, daily at 10 pm
45 22 * * * /data/predict1/utility/dpimport_avlqc.sh /data/predict1/data_from_nda_dev/ dpstage

# generate difference between AMP-SCZ and network data dictionaries
0 6 * * * /data/predict1/utility/_gen_dict_diff.sh 123456 123456 123456 tbillah sbouix gjacobs1



# === dn001 ===

# PRESCIENT real
# determine if new and upload to REDCap
0 18 * * * /data/predict1/miniconda3/bin/python /data/predict1/utility/set_rpms_date_shifts.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ "*/raw/*/surveys/" && /data/predict1/utility/_rpms_to_redcap.sh /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED /data/predict1/utility/rpms-to-yale 123456

# keep six hours difference between upload and download so upload can complete

# clean old arms, download JSONs from REDCap and shift their dates
59 23 * * * /data/predict1/utility/clean_down_shift.sh 123456


# ProNET real
# determine if new and shift dates
# determine if new and upload to REDCap
00 22 * * * umask 0007 && /data/predict1/utility/_shift_redcap_dates.sh /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED "*/raw/*/surveys/*.Pronet.json" /data/predict1/utility/yale-real/CloneOfYaleRealRecords_DataDictionary_2023-09-04_checkbox.csv && /data/predict1/utility/_records_to_redcap.sh /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED /data/predict1/utility/yale-real 123456


# mongodb backup
0 8 * * * /data/predict1/utility/backup_mongodb.sh rc-predict


# kill stale processes every other day
0 14 * * */2 pkill -u tb571 python


# === dn018 ===

# upload data tracker CSV files to Dropbox
0 4 * * * /data/predict1/utility/data_tracker_dropbox.sh

# track /data/predict1/ size, every monday at 12 am
0 0 * * 1 /data/predict1/utility/track_briefcase_size.sh /data/predict1/ tbillah sbouix jtbaker



# === dn003 ===

# clear REDCap upload logs, every Friday at 5 pm
0 17 * * 5 rm -f /data/predict1/utility/bsub/*

# clear NDA upload logs every Monday at 12 am
0 0 * * 1 rm -rf /PHShome/tb571/NDA/nda-tools/vtcmd/*/*

# download EEG run sheets
# every morning at 3 am
0 3 * * * /data/predict1/eeg-qc-dash/down_eeg_pdf_rsheet.sh 123456 /data/predict1/data_from_nda/Pronet
# every morning at 4 am
0 4 * * * /data/predict1/eeg-qc-dash/down_eeg_pdf_rsheet.sh 123456 /data/predict1/data_from_nda/Prescient



# === dn020 ===

# copy EEG QC images over to web app VM
0 4 * * * /data/predict1/utility/rsync_eegqc.sh /data/predict1/data_from_nda/ /data/eegqc/
0 5 * * * /data/predict1/utility/rsync_eegqc.sh /data/predict1/kcho/flow_test/spero/ /opt/data/eegqc-mock/

0 05 * * * /data/predict1/utility/backup_formqc.sh

# === rc-predict-gen ===

# back up EEG QC web app scores
# run as service account
22 15 * * * /opt/eeg-qc-dash/backup_scores.cron /data/eegqc/ /opt/data/eegqc-mock/
0 0 * * * rsync -a /data/eegqc/.scores.pkl eris2n4.research.partners.org:/data/predict1/data_from_nda/



# === rc-predict ===

# track / size, every day at 12 am
0 0 * * * /opt/track_briefcase_size.sh / tbillah sbouix jtbaker

# generate list of DPdash users
# run as root
0 8 * * * /opt/dpdash/dpdash/get_dpdash_accounts.sh tbillah sbouix ekotler



# === 1200941-Prescient.orygen.org.au ===

SHELL=/bin/bash
HOSTNAME=1200941-Prescient.orygen.org.au

MAILTO=xyz@bwh.harvard.edu
03 20 * * * /mnt/prescient/utility/rpms_cron.sh



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



# all dpimport are run by tb571 in dn020
# TODO run by sf284
# import all data to production DPdash in succession
0 19 * * * /data/predict1/utility/dpimport_avlqc.sh /data/predict1/data_from_nda/ rc-predict
0 20 * * * /data/predict1/utility/dpimport_formqc.sh /data/predict1/data_from_nda/ rc-predict > /data/predict1/utility/dpimport_formqc.log.txt 2>&1
0 00 * * * /data/predict1/utility/dpimport_digital.sh /data/predict1/data_from_nda/ rc-predict
0 02 * * * /data/predict1/utility/dpimport_mriqc.sh /data/predict1/data_from_nda/ rc-predict
0 03 * * * /data/predict1/utility/dpimport_eegqc.sh /data/predict1/data_from_nda/ rc-predict
0 06 * * * /data/predict1/utility/generate_files_status1.sh /data/predict1/data_from_nda/ rc-predict
