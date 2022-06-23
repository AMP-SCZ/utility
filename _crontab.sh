# generate lochness datalake's files status hourly for dpdash, hourly
20 * * * * /data/predict/utility/generate_files_status.sh /data/predict/data_from_nda/ rc-predict
25 * * * * /data/predict/utility/generate_files_status.sh /data/predict/data_from_nda_dev/ dpstage

# import AVL QC data, daily at 4 pm
00 16 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/data_from_nda/ rc-predict
05 16 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/data_from_nda_dev/ dpstage

# clear REDCap upload logs, every monday at 12 am
0 * * * 1 rm -f /data/predict/utility/bsub/*

# import records to REDCap, every third hour
# PRESCIENT mock
0 */3 * * * /data/predict/utility/records_to_redcap.sh /data/predict/data_from_nda_dev/Prescient/PHOENIX/PROTECTED /data/predict/utility/amp-scz-form 123456

# ProNET mock
20 */3 * * * /data/predict/utility/records_to_redcap.sh /data/predict/data_from_nda_dev/Pronet/PHOENIX/PROTECTED /data/predict/utility/redcap-ii-yale 123456

# ProNET real
40 */3 * * * /data/predict/utility/records_to_redcap.sh /data/predict/data_from_nda/Pronet/PHOENIX/PROTECTED /data/predict/utility/yale-real 123456
