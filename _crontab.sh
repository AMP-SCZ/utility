# generate lochness datalake's files status hourly for dpdash, hourly
20 * * * * /data/predict/utility/generate_files_status.sh /data/predict/data_from_nda/ rc-predict
25 * * * * /data/predict/utility/generate_files_status.sh /data/predict/data_from_nda_dev/ dpstage

# import AVL QC data, daily at 4 pm
00 16 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/data_from_nda/ rc-predict
05 16 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/data_from_nda_dev/ dpstage

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
0 23 * * * /data/predict/utility/_shift_redcap_dates.sh /data/predict/data_from_nda/Pronet/PHOENIX/PROTECTED "*/raw/*/surveys/*.Pronet.json" /data/predict/utility/yale-real/ProNETPsychosisRiskOutcomesNet_DataDictionary_2022-10-28_checkbox.csv
0 0 * * 3 /data/predict/utility/_records_to_redcap.sh /data/predict/data_from_nda/Pronet/PHOENIX/PROTECTED /data/predict/utility/yale-real 123456


