#!/bin/bash
set -e

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
./wais_iv_part101.sh wisc_v01_${n}_baseline.csv


# individual group
./generate.sh -n $n -f socdem01 -p chrdemo
./generate.sh -n $n -f cgis01 -e baseline

# have outcome variables
./generate.sh -n $n -f ampscz_psychs01 -e screening -p chrpsychs_scr
./generate.sh -n $n -f ampscz_psychs01 -e baseline -p chrpsychs_fu
./generate.sh -n $n -f ampscz_nsipr01 -e baseline
./generate.sh -n $n -f bprs01 -e baseline -p chrbprs
./generate.sh -n $n -f clgry01 -e baseline -p chrcdss
./generate.sh -n $n -f cssrs01 -e baseline -p chrcssrsb
./generate.sh -n $n -f dsm_iv_es01 -e screening -p chrsofas
./generate.sh -n $n -f gfs01 -e baseline -p chrgfrs
./generate.sh -n $n -f gfs01 -e baseline -p chrgfss
./generate.sh -n $n -f oasis01 -e baseline -p chroasis
./generate.sh -n $n -f pmod01 -e baseline -p chrpreiq
./generate.sh -n $n -f sri01 -e baseline -p chrpromis
./generate.sh -n $n -f pss01 -e baseline -p chrpss

# no -e or -p required
./generate.sh -n $n -f ampscz_dim01
./generate.sh -n $n -f ampscz_rap01 -e baseline
./generate.sh -n $n -f ampscz_rs01
./generate.sh -n $n -f iec01 
./generate.sh -n $n -f pds01
./_figs01.sh $n


done

exit

### combination step ###
for f in assist01 ampscz_iqa01 wasi201 wisc_v01 ampscz_psychs01 ampscz_nsipr01 bprs01 clgry01 cssrs01 oasis01 pmod01 sri01 pss01 ampscz_rap01
do
    ./combine_networks.sh -f $f -e baseline
done

for f in ampscz_hcgfb01 ampscz_lapes01 scidvapd01 tbi01 dsm_iv_es01 ampscz_psychs01
do
    ./combined_networks.sh -f $f -e screening
done

for f in ampscz_dim01 ampscz_rs01 iec01 pds01 figs01
do
   ./combined_networks.sh -f $f
done


