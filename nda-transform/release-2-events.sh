#!/bin/bash
set -e

for n in Pronet
do

./generate.sh -n $n -e screening -f ampscz_rs01
./generate.sh -n $n -e screening -f ampscz_lapes01   -p chrap -o "--interview_date_var chrap_date"
./generate.sh -n $n -e screening -f medhi01          -p chrpharm
./generate.sh -n $n -e screening -f iec01
./generate.sh -n $n -e screening -f ampscz_hcgfb01   -p chrhealth
./generate.sh -n $n -e screening -f scidvapd01       -p chrschizotypal
./generate.sh -n $n -e screening -f tbi01            -p chrtbi
./generate.sh -n $n -e screening -f dsm_iv_es01      -p chrsofas
./generate.sh -n $n -e screening -f ampscz_psychs01  -p chrpsychs_scr

./generate.sh -n $n -e baseline  -f socdem01         -p chrdemo
./generate.sh -n $n -e baseline  -f dsm_iv_es01      -p chrsofas -o "--interview_date_var chrsofas_interview_date_fu --follow"
./generate.sh -n $n -e baseline  -f ampscz_psychs01  -p chrpsychs_fu
./generate.sh -n $n -e baseline  -f ampscz_iqa01     -p chriq
./generate.sh -n $n -e baseline  -f wasi201          -p chriq
./generate.sh -n $n -e baseline  -f wisc_v01         -p chriq
./generate.sh -n $n -e baseline  -f pmod01           -p chrpreiq
./generate.sh -n $n -e baseline  -f vitas01          -p chrchs
./generate.sh -n $n -e baseline  -f dailyd01         -p chrsaliva
./generate.sh -n $n -e baseline  -f clinlabtestsp201 -p chrcbc
./generate.sh -n $n -e baseline  -f ampscz_nsipr01
./generate.sh -n $n -e baseline  -f clgry01          -p chrcdss
./generate.sh -n $n -e baseline  -f assist01         -p chrassist
./generate.sh -n $n -e baseline  -f cssrs01          -p chrcssrsb
./generate.sh -n $n -e baseline  -f gfs01            -p chrgfss
./generate.sh -n $n -e baseline  -f gfs01            -p chrgfrs
./generate.sh -n $n -e baseline  -f ampscz_dim01
./generate.sh -n $n -e baseline  -f pds01
./generate.sh -n $n -e baseline  -f oasis01          -p chroasis
./generate.sh -n $n -e baseline  -f sri01            -p chrpromis
./generate.sh -n $n -e baseline  -f pss01            -p chrpss
./generate.sh -n $n -e baseline  -f ampscz_pps01     -p chrpps
./generate.sh -n $n -e baseline  -f cgis01
./generate.sh -n $n -e baseline  -f bprs01           -p chrbprs
./generate.sh -n $n -e baseline  -f ampscz_rap01

./generate.sh -n $n -e month_1   -f dsm_iv_es01      -p chrsofas -o "--interview_date_var chrsofas_interview_date_fu --follow"
./generate.sh -n $n -e month_1   -f ampscz_psychs01  -p chrpsychs_fu
./generate.sh -n $n -e month_1   -f pmod01           -p chrpas
./generate.sh -n $n -e month_1   -f ampscz_nsipr01
./generate.sh -n $n -e month_1   -f clgry01          -p chrcdss
./generate.sh -n $n -e month_1   -f gfs01            -p chrgfssfu
./generate.sh -n $n -e month_1   -f gfs01            -p chrgfrsfu
./generate.sh -n $n -e month_1   -f oasis01          -p chroasis
./generate.sh -n $n -e month_1   -f pss01            -p chrpss
./generate.sh -n $n -e month_1   -f cgis01
./generate.sh -n $n -e month_1   -f bprs01           -p chrbprs

./generate.sh -n $n -e month_2   -f dsm_iv_es01      -p chrsofas -o "--interview_date_var chrsofas_interview_date_fu --follow"
./generate.sh -n $n -e month_2   -f ampscz_psychs01  -p chrpsychs_fu
./generate.sh -n $n -e month_2   -f vitas01          -p chrchs
./generate.sh -n $n -e month_2   -f dailyd01         -p chrsaliva
./generate.sh -n $n -e month_2   -f clinlabtestsp201 -p chrcbc
./generate.sh -n $n -e month_2   -f ampscz_nsipr01
./generate.sh -n $n -e month_2   -f clgry01          -p chrcdss
./generate.sh -n $n -e month_2   -f assist01         -p chrassist
./generate.sh -n $n -e month_2   -f cssrs01          -p chrcssrsfu
./generate.sh -n $n -e month_2   -f gfs01            -p chrgfssfu
./generate.sh -n $n -e month_2   -f gfs01            -p chrgfrsfu
./generate.sh -n $n -e month_2   -f oasis01          -p chroasis
./generate.sh -n $n -e month_2   -f sri01            -p chrpromis
./generate.sh -n $n -e month_2   -f pss01            -p chrpss
./generate.sh -n $n -e month_2   -f cgis01
./generate.sh -n $n -e month_2   -f bprs01           -p chrbprs

done