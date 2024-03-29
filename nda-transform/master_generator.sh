#!/bin/bash
set -e


if [ "$1" == "generate" ]
then

### generation step ###

for n in Pronet Prescient
do

# assist01 group
./generate.sh -n $n -f assist01 -e baseline -p chrassist
./generate.sh -n $n -f ampscz_iqa01 -e baseline -p chriq
./generate.sh -n $n -f ampscz_hcgfb01 -e screening -p chrhealth
./generate.sh -n $n -f ampscz_lapes01 -e screening -p chrap -o "--interview_date_var chrap_date"
./generate.sh -n $n -f scidvapd01 -e screening -p chrschizotypal


# tbi01 group
./generate.sh -n $n -f tbi01 -e screening -p chrtbi
./generate.sh -n $n -f wasi201 -e baseline -p chriq
./generate.sh -n $n -f wisc_v01 -e baseline -p chriq
# ./wais_iv_part101.sh wisc_v01_${n}_baseline.csv


# individual group
./generate.sh -n $n -f socdem01 -p chrdemo
./generate.sh -n $n -f cgis01 -e baseline
./generate.sh -n $n -f ampscz_rap01 -e baseline
./generate.sh -n $n -f ampscz_pps01 -e baseline -p chrpps


# have outcome variables
./generate.sh -n $n -f ampscz_psychs01 -e screening -p chrpsychs_scr
./generate.sh -n $n -f ampscz_psychs01 -e baseline -p chrpsychs_fu
./generate.sh -n $n -f ampscz_nsipr01 -e baseline
./generate.sh -n $n -f bprs01 -e baseline -p chrbprs
./generate.sh -n $n -f clgry01 -e baseline -p chrcdss
./generate.sh -n $n -f cssrs01 -e baseline -p chrcssrsb
./generate.sh -n $n -f dsm_iv_es01 -e screening -p chrsofas
./generate.sh -n $n -f dsm_iv_es01 -e baseline -p chrsofas -o "--interview_date_var chrsofas_interview_date_fu --follow"
./generate.sh -n $n -f gfs01 -e baseline -p chrgfrs
./generate.sh -n $n -f gfs01 -e baseline -p chrgfss
./generate.sh -n $n -f oasis01 -e baseline -p chroasis
./generate.sh -n $n -f pmod01 -e baseline -p chrpreiq
./generate.sh -n $n -f sri01 -e baseline -p chrpromis
./generate.sh -n $n -f pss01 -e baseline -p chrpss

# no -e or -p required
./generate.sh -n $n -f ampscz_dim01
./generate.sh -n $n -f ampscz_rs01
./generate.sh -n $n -f iec01 
./generate.sh -n $n -f pds01
./_figs01.sh $n


# structures after release-1
./generate.sh -n $n -f medhi01 -e screening -p chrpharm

./generate.sh -n $n -f clinlabtestsp201 -e baseline -p chrcbc
./generate.sh -n $n -f vitas01 -e baseline -p chrchs
./generate.sh -n $n -f dailyd01 -e baseline -p chrsaliva
./generate.sh -n $n -f scidcls01 -e baseline -p chrscid

done


elif [ "$1" == "combine" ]
then

### combination step ###

for f in assist01 ampscz_iqa01 wasi201 wisc_v01 cgis01 ampscz_rap01 ampscz_pps01 ampscz_psychs01 ampscz_nsipr01 bprs01 clgry01 cssrs01 dsm_iv_es01 oasis01 pmod01 sri01 pss01 clinlabtestsp201 vitas01 dailyd01 scidcls01
do
    ./combine_networks.sh -f $f -e baseline
done

for f in ampscz_hcgfb01 ampscz_lapes01 scidvapd01 tbi01 dsm_iv_es01 ampscz_psychs01 medhi01
do
    ./combine_networks.sh -f $f -e screening
done

for f in socdem01 ampscz_dim01 ampscz_rs01 iec01 pds01 figs01
do
   ./combine_networks.sh -f $f
done

./combine_networks.sh -f gfs01 -e baseline -s chrgfss
./combine_networks.sh -f gfs01 -e baseline -s chrgfrs

./wais_iv_part101.sh /data/predict1/to_nda/nda-submissions/network_combined/wisc_v01_baseline.csv

else

echo """Usage:
$0 generate
$0 combine"""

fi

