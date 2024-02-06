#!/bin/bash

# script for conveniently resubmitting form data

for i in ndar_subject01 socdem01; do ./submit.sh -f $i -u tbillah; done

for i in ampscz_hcgfb01 ampscz_lapes01 scidvapd01 tbi01; do ./submit.sh -f $i -u tbillah -e screening; done

for i in ampscz_iqa01 ampscz_pps01 ampscz_rap01 assist01 cgis01 wais_iv_part101 wasi201 wisc_v01; do ./submit.sh -f $i -u tbillah -e baseline; done

