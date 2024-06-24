# generate files status every day
0 17 * * * /data/predict1/utility/generate_files_status1.sh /data/predict1/data_from_nda/

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

# recess is on Tuesday, Thursday, Monday

