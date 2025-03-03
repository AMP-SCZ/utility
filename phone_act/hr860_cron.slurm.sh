0 20 * * 1,3,5 /data/predict1/utility/phone_act/dpcron.slurm.sh -n Pronet -m "phone_accel phone_survey phone_survey_nda phone_power data_availmg"
0 20 * * 1,3,5 /data/predict1/utility/phone_act/dpcron.slurm.sh -n Pronet -m "parse_gps_mc preprocess_gps_mc process_gps_mc aggregate_gps_mc phone_gps_mc"
0 20 * * 1,3,5 /data/predict1/utility/phone_act/dpcron.slurm.sh -n Pronet -m "geneactiv_extract_ax geneactiv_freq geneactiv_act geneactiv_sync_mc geneactiv_qcact geneactiv_upact"

0 19 * * 1,3,5 pkill -f "/data/sbdp/dphtool/*.py"

0 17 * * 2,4,6 /data/predict1/utility/phone_act/dpcron.slurm.sh -n Prescient -m "phone_accel phone_survey phone_survey_nda phone_power data_availmg"
0 17 * * 2,4,6 /data/predict1/utility/phone_act/dpcron.slurm.sh -n Prescient -m "parse_gps_mc preprocess_gps_mc process_gps_mc aggregate_gps_mc phone_gps_mc"
0 17 * * 2,4,6 /data/predict1/utility/phone_act/dpcron.slurm.sh -n Prescient -m "geneactiv_extract_ax geneactiv_freq geneactiv_act geneactiv_sync_mc geneactiv_qcact geneactiv_upact"
