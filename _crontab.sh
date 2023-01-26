# PREDICT cron jobs are distributed among servers to optimally use their bandwidth & loading
# log in to each server and type crontab -e to view/edit them



# === hna002 ===

# generate lochness datalake's files status at 6 am and 9pm for dpdash
00 6,21 * * * * /data/predict/utility/generate_files_status.sh /data/predict/data_from_nda/ rc-predict
30 6,21 * * * * /data/predict/utility/generate_files_status.sh /data/predict/data_from_nda_dev/ dpstage

# import AVL QC data, daily at 10 pm
30 22 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/data_from_nda/ rc-predict
45 22 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/data_from_nda_dev/ dpstage

# generate difference between AMP-SCZ and network data dictionaries
0 6 * * * /data/predict/utility/_gen_dict_diff.sh 123456 123456 123456 tbillah sbouix gjacobs1



# === eris2n4 ===

# clear REDCap upload logs, every monday at 12 am
0 * * * 1 rm -f /data/predict/utility/bsub/*

# import records to REDCap, once a week
# used to be 0 */3, 15 */3, 30 */3, 45 */3 (every three hours)
# changed to only once a week to unburden the compute nodes
# PRESCIENT mock
0 0 * * 0 /data/predict/utility/_rpms_to_redcap.sh /data/predict/data_from_nda_dev/Prescient/PHOENIX/PROTECTED /data/predict/utility/amp-scz-form 123456

# PRESCIENT real
0 0 * * 1 /data/predict/utility/_rpms_to_redcap.sh /data/predict/data_from_nda/Prescient/PHOENIX/PROTECTED /data/predict/utility/amp-scz-form 123456

# ProNET mock
0 0 * * 2 /data/predict/utility/_records_to_redcap.sh /data/predict/data_from_nda_dev/Pronet/PHOENIX/PROTECTED /data/predict/utility/redcap-ii-yale 123456

# ProNET real
0 22 * * * /data/predict/utility/_shift_redcap_dates.sh /data/predict/data_from_nda/Pronet/PHOENIX/PROTECTED "*/raw/*/surveys/*.Pronet.json" /data/predict/utility/yale-real/ProNETPsychosisRiskOutcomesNet_DataDictionary_2022-10-28_checkbox.csv && /data/predict/utility/_records_to_redcap.sh /data/predict/data_from_nda/Pronet/PHOENIX/PROTECTED /data/predict/utility/yale-real 123456



# === eris2n5 ===

# download EEG run sheets
# every morning at 3 am
0 3 * * * /data/predict/eeg-qc-dash/down_eeg_pdf_rsheet.sh 123456 /data/predict/data_from_nda/Pronet
# every morning at 4 am
0 4 * * * /data/predict/eeg-qc-dash/down_eeg_pdf_rsheet.sh 123456 /data/predict/data_from_nda/Prescient



# === dn020 ===

# copy EEG QC images over to web app VM
0 4 * * * /data/predict/utility/rsync_eegqc.sh /data/predict/data_from_nda/ /data/eegqc/
0 5 * * * /data/predict/utility/rsync_eegqc.sh /data/predict/kcho/flow_test/spero/ /opt/data/eegqc-mock/



# === rc-predict-gen ===

# back up EEG QC web app scores
# run as service account
22 15 * * * /opt/eeg-qc-dash/backup_scores.cron /data/eegqc/ /opt/data/eegqc-mock/



# === rc-predict ===

# generate list of DPdash users
# run as root
0 8 * * * /opt/dpdash/dpdash/get_dpdash_accounts.sh tbillah sbouix ekotler



# === 1200941-Prescient.orygen.org.au ===

SHELL=/bin/bash
HOSTNAME=1200941-Prescient.orygen.org.au

MAILTO=xyz@bwh.harvard.edu
04 20 * * * /usr/bin/rm /mnt/prescient/one_day_backup/* && /usr/bin/cp /mnt/prescient/RPMS_incoming/*csv /mnt/prescient/one_day_backup/
05 20 * * * /home/tashrifbillah/miniconda3/bin/python /mnt/prescient/utility/rename_RPMS_vars.py /mnt/prescient/RPMS_incoming/
07 20 * * * /home/tashrifbillah/miniconda3/bin/python /mnt/prescient/utility/replace_RPMS_values.py /mnt/prescient/RPMS_incoming/
10 20 * * * /home/tashrifbillah/miniconda3/bin/python /mnt/prescient/utility/rpms_psychs_partition.py /mnt/prescient/RPMS_incoming/

