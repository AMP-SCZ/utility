#!/bin/bash

# listserv generator for mailx
# from is tbillah, to is tkapur
# all other recipients are in bcc
# just execute this script at rc-predict.partners.org:
# cd /opt/dpdash/dpdash/ && ./generate_listserv.sh

IFS=$'\n'

echo
echo -n " -r tbillah_email "

for line in $(cat users/dpdash_users_$(date +"%Y%m%d").csv)
do
    IFS=, read -ra props <<< "$line"

    # an entry is a valid email if it has @text.
    email=`echo ${props[2]} | grep "\@.*\."`

    if [ ! -z $email ]
    then
        echo -n "-b $email "
    fi

done

echo "-- tkapur_email"
echo


