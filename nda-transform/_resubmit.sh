#!/bin/bash

# script for conveniently resubmitting form data

for i in ndar_subject01 socdem01; do ./submit.sh -f $i -u tbillah; done

for i in ampscz_hcgfb01 ampscz_lapes01 scidvapd01 tbi01; do ./submit.sh -f $i -u tbillah -e screening; done

for i in ampscz_iqa01 ampscz_pps01 ampscz_rap01 assist01 cgis01 wais_iv_part101 wasi201 wisc_v01; do ./submit.sh -f $i -u tbillah -e baseline; done

for f in ampscz_dim01 ampscz_rs01 iec01 pds01 figs01; do ./submit.sh -f $f -u tbillah; done


./submit.sh -f gfs01 -s chrgfss -e baseline -u tbillah
./submit.sh -f gfs01 -s chrgfrs -e baseline -u tbillah


for f in ampscz_psychs01 ampscz_nsipr01 bprs01 clgry01 cssrs01 dsm_iv_es01 oasis01 pmod01 sri01 pss01
do
    ./submit.sh -f $f -e baseline -u tbillah
done


for f in ampscz_psychs01 dsm_iv_es01
do
    ./combine_networks.sh -f $f -e screening
done

