# generate lochness datalake's files status hourly for dpdash, hourly
20 * * * * /data/predict/utility/generate_files_status.sh /data/predict/data_from_nda/ rc-predict
25 * * * * /data/predict/utility/generate_files_status.sh /data/predict/kcho/flow_test/ dpstage

# import AVL QC data, daily at 4 pm
0 16 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/data_from_nda/ rc-predict
0 16 * * * /data/predict/utility/dpimport_avlqc.sh /data/predict/kcho/flow_test/ dpstage

# populate clone of site records, daily at 6 am
0 6 * * * /data/predict/utility/_records_to_redcap.sh

