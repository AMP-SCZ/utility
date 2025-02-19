#!/bin/bash
set -e

if [ "$1" == generate ]
then

for n in Pronet Prescient
do

./generate.sh -n $n -e screening -f ampscz_rs01
./generate.sh -n $n -e screening -f ampscz_lapes01   -p chrap -o "--interview_date_var chrap_date"
./generate.sh -n $n -e screening -f medhi01          -p chrpharm
./generate.sh -n $n -e screening -f iec01
./generate.sh -n $n -e screening -f ampscz_hcgfb01   -p chrhealth
./generate.sh -n $n -e screening -f scidvapd01       -p chrschizotypal
./generate.sh -n $n -e screening -f tbi01            -p chrtbi
./generate.sh -n $n -e screening -f figs01           -p chrfigs
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
./generate.sh -n $n -e baseline  -f scidcls01        -p chrscid

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

elif [ "$1" == combine ]
then

./combine_networks.sh              -f ampscz_rs01      
./combine_networks.sh -e screening -f ampscz_lapes01   
./combine_networks.sh -e screening -f medhi01          
./combine_networks.sh              -f iec01            
./combine_networks.sh -e screening -f ampscz_hcgfb01   
./combine_networks.sh -e screening -f scidvapd01       
./combine_networks.sh -e screening -f tbi01            
./combine_networks.sh              -f figs01           
./combine_networks.sh -e screening -f dsm_iv_es01      
./combine_networks.sh -e screening -f ampscz_psychs01  

./combine_networks.sh              -f socdem01         
./combine_networks.sh -e baseline  -f dsm_iv_es01      
./combine_networks.sh -e baseline  -f ampscz_psychs01  
./combine_networks.sh -e baseline  -f ampscz_iqa01     
./combine_networks.sh -e baseline  -f wasi201          
./combine_networks.sh -e baseline  -f wisc_v01         
./wais_iv_part101.sh  -e baseline  

./combine_networks.sh -e baseline  -f pmod01           
./combine_networks.sh -e baseline  -f vitas01          
./combine_networks.sh -e baseline  -f dailyd01         
./combine_networks.sh -e baseline  -f clinlabtestsp201 
./combine_networks.sh -e baseline  -f ampscz_nsipr01   
./combine_networks.sh -e baseline  -f clgry01          
./combine_networks.sh -e baseline  -f assist01         
./combine_networks.sh -e baseline  -f cssrs01          
./combine_networks.sh -e baseline  -f gfs01            -s chrgfss
./combine_networks.sh -e baseline  -f gfs01            -s chrgfrs
./combine_networks.sh              -f ampscz_dim01     
./combine_networks.sh              -f pds01            
./combine_networks.sh -e baseline  -f oasis01          
./combine_networks.sh -e baseline  -f sri01            
./combine_networks.sh -e baseline  -f pss01            
./combine_networks.sh -e baseline  -f ampscz_pps01     
./combine_networks.sh -e baseline  -f cgis01           
./combine_networks.sh -e baseline  -f bprs01           
./combine_networks.sh -e baseline  -f ampscz_rap01     
./combine_networks.sh -e baseline  -f scidcls01

./combine_networks.sh -e month_1   -f dsm_iv_es01      
./combine_networks.sh -e month_1   -f ampscz_psychs01  
./combine_networks.sh -e month_1   -f pmod01           
./combine_networks.sh -e month_1   -f ampscz_nsipr01   
./combine_networks.sh -e month_1   -f clgry01          
./combine_networks.sh -e month_1   -f gfs01            -s chrgfssfu
./combine_networks.sh -e month_1   -f gfs01            -s chrgfrsfu
./combine_networks.sh -e month_1   -f oasis01          
./combine_networks.sh -e month_1   -f pss01            
./combine_networks.sh -e month_1   -f cgis01           
./combine_networks.sh -e month_1   -f bprs01           

./combine_networks.sh -e month_2   -f dsm_iv_es01      
./combine_networks.sh -e month_2   -f ampscz_psychs01  
./combine_networks.sh -e month_2   -f vitas01          
./combine_networks.sh -e month_2   -f dailyd01         
./combine_networks.sh -e month_2   -f clinlabtestsp201 
./combine_networks.sh -e month_2   -f ampscz_nsipr01   
./combine_networks.sh -e month_2   -f clgry01          
./combine_networks.sh -e month_2   -f assist01         
./combine_networks.sh -e month_2   -f cssrs01          
./combine_networks.sh -e month_2   -f gfs01            -s chrgfssfu
./combine_networks.sh -e month_2   -f gfs01            -s chrgfrsfu
./combine_networks.sh -e month_2   -f oasis01          
./combine_networks.sh -e month_2   -f sri01            
./combine_networks.sh -e month_2   -f pss01            
./combine_networks.sh -e month_2   -f cgis01           
./combine_networks.sh -e month_2   -f bprs01           

elif [ "$1" == submit ]
then

./submit.sh -u tbillah              -f ampscz_rs01      
./submit.sh -u tbillah -e screening -f ampscz_lapes01   
./submit.sh -u tbillah -e screening -f medhi01          
./submit.sh -u tbillah              -f iec01            
./submit.sh -u tbillah -e screening -f ampscz_hcgfb01   
./submit.sh -u tbillah -e screening -f scidvapd01       
./submit.sh -u tbillah -e screening -f tbi01            
./submit.sh -u tbillah              -f figs01           
./submit.sh -u tbillah -e screening -f dsm_iv_es01      
./submit.sh -u tbillah -e screening -f ampscz_psychs01  

./submit.sh -u tbillah              -f socdem01         
./submit.sh -u tbillah -e baseline  -f dsm_iv_es01      
./submit.sh -u tbillah -e baseline  -f ampscz_psychs01  
./submit.sh -u tbillah -e baseline  -f ampscz_iqa01     
./submit.sh -u tbillah -e baseline  -f wasi201          
./submit.sh -u tbillah -e baseline  -f wisc_v01         
./submit.sh -u tbillah -e baseline  -f wais_iv_part101  

./submit.sh -u tbillah -e baseline  -f pmod01           
./submit.sh -u tbillah -e baseline  -f vitas01          
./submit.sh -u tbillah -e baseline  -f dailyd01         
./submit.sh -u tbillah -e baseline  -f clinlabtestsp201 
./submit.sh -u tbillah -e baseline  -f ampscz_nsipr01   
./submit.sh -u tbillah -e baseline  -f clgry01          
./submit.sh -u tbillah -e baseline  -f assist01         
./submit.sh -u tbillah -e baseline  -f cssrs01          
./submit.sh -u tbillah -e baseline  -f gfs01            -s chrgfss
./submit.sh -u tbillah -e baseline  -f gfs01            -s chrgfrs
./submit.sh -u tbillah              -f ampscz_dim01     
./submit.sh -u tbillah              -f pds01            
./submit.sh -u tbillah -e baseline  -f oasis01          
./submit.sh -u tbillah -e baseline  -f sri01            
./submit.sh -u tbillah -e baseline  -f pss01            
./submit.sh -u tbillah -e baseline  -f ampscz_pps01     
./submit.sh -u tbillah -e baseline  -f cgis01           
./submit.sh -u tbillah -e baseline  -f bprs01           
./submit.sh -u tbillah -e baseline  -f ampscz_rap01     

./submit.sh -u tbillah -e month_1   -f dsm_iv_es01      
./submit.sh -u tbillah -e month_1   -f ampscz_psychs01  
./submit.sh -u tbillah -e month_1   -f pmod01           
./submit.sh -u tbillah -e month_1   -f ampscz_nsipr01   
./submit.sh -u tbillah -e month_1   -f clgry01          
./submit.sh -u tbillah -e month_1   -f gfs01            -s chrgfssfu
./submit.sh -u tbillah -e month_1   -f gfs01            -s chrgfrsfu
./submit.sh -u tbillah -e month_1   -f oasis01          
./submit.sh -u tbillah -e month_1   -f pss01            
./submit.sh -u tbillah -e month_1   -f cgis01           
./submit.sh -u tbillah -e month_1   -f bprs01           

./submit.sh -u tbillah -e month_2   -f dsm_iv_es01      
./submit.sh -u tbillah -e month_2   -f ampscz_psychs01  
./submit.sh -u tbillah -e month_2   -f vitas01          
./submit.sh -u tbillah -e month_2   -f dailyd01         
./submit.sh -u tbillah -e month_2   -f clinlabtestsp201 
./submit.sh -u tbillah -e month_2   -f ampscz_nsipr01   
./submit.sh -u tbillah -e month_2   -f clgry01          
./submit.sh -u tbillah -e month_2   -f assist01         
./submit.sh -u tbillah -e month_2   -f cssrs01          
./submit.sh -u tbillah -e month_2   -f gfs01            -s chrgfssfu
./submit.sh -u tbillah -e month_2   -f gfs01            -s chrgfrsfu
./submit.sh -u tbillah -e month_2   -f oasis01          
./submit.sh -u tbillah -e month_2   -f sri01            
./submit.sh -u tbillah -e month_2   -f pss01            
./submit.sh -u tbillah -e month_2   -f cgis01           
./submit.sh -u tbillah -e month_2   -f bprs01           

fi

