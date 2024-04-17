#!/bin/sh

if [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ $# == 0 ] 
then
    echo """Usage:
$0 /path/to/out/dir
This script will loop over sites and extract phone type/version from each MindLAMP raw .json and save in out dir.
/data/predict1/mindlamp_phoneOS_Mar2024 (2024 March Release)
"""
    exit
fi

out=$1
mkdir -p $out || exit

tolerance=5
Pronet_sites="PronetBI  PronetCM  PronetHA  PronetKC  PronetMA  PronetMU  PronetNL  PronetOH  PronetPA  PronetPV  PronetSF  PronetSL  PronetUR  PronetYA PronetCA  PronetGA  PronetIR  PronetLA  PronetMT  PronetNC  PronetNN  PronetOR  PronetPI  PronetSD  PronetSI  PronetTE  PronetWU"

Prescient_sites="PrescientBM PrescientCG PrescientCP PrescientGW PrescientHK PrescientJE PrescientLS PrescientME PrescientSG"

for site in $Prescient_sites $Pronet_sites  
do
	ispronet=`echo $site | grep Pronet | wc -l`
	isprescient=`echo $site | grep Prescient | wc -l`

	echo ""
	echo "--------------------------------------------------------------------"
	if [ $ispronet -gt 0 ]
	then
		echo "$site is Pronet" 
		raw="/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/${site}/raw"
	elif [ $isprescient -gt 0 ]
	then
		echo "$site is Prescient"
		raw="/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/${site}/raw"
	else
		echo "I don't understand"
	fi

	cd $raw
	for id in `ls`
	do 
		if [ -e ${id}/phone ]
		then
			jsoncnt=`ls ${id}/phone/*json | wc -l`
			firstjson=`ls ${id}/phone/*json | head -1`
			lastjson=`ls ${id}/phone/*json | tail -1`
			printf "Parsing $jsoncnt JSONs ( `basename $firstjson` to `basename $lastjson` ) for ${id}:"

			file=${out}/${site}-${id}-mindlamp_phoneOS.txt
			if [ -e $file ]
			then
				#if [ `cat $file | wc -l` -lt $tolerance ]
				#then
					echo "Existing $file is `cat $file | wc -l` lines long...removing."
					rm $file
				#fi 
			fi
		
			if [ ! -e $file ]
			then
				cd ${raw}/${id}/phone/ 

				for json in `ls *json`
				do 
					printf "."	
					if [ `grep user_agent $json | wc -l` -gt 0 ]
					then 
						date=`echo $json | sed 's/.json//' | awk -F '_' '{printf("%s/%s/%s ",$5,$6,$4)}'`  

						OS=`grep user_agent $json | sed 's/,\([^,]*\)$/ \1/' | awk -F ';' '{print $2}' | grep -v CPU | sort -u | awk '{printf("%s ",$0)}' ` 
						if [ `echo $OS | grep iOS | wc -w` -gt 0 ]
						then
							phone=`grep user_agent $json | sed 's/,\([^,]*\)$/ \1/' | awk -F ';' '{print $3}' | sort -u | tail -1 | sed 's/\"\([^\"]*\)$/ \1/'`
						else
							phone=`grep user_agent $json | sed 's/,\([^,]*\)$/ \1/' | awk -F ';' '{print $3}' | sort -u | tail -1`
						fi
						printf "."

						printf "$id ; $date ; $OS ; $phone\n" >> ${out}/${site}-${id}-mindlamp_phoneOS.txt
					fi 
				done
				echo ""
			else
				echo "using existing"
			fi
			echo ""
			cat $file
			echo ""
		else 
			echo "$id NO PHONE"
		fi
		cd ${raw}
	done
	echo ""
done
