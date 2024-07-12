#!/bin/bash

# running at predict VM
# 0 8 * * * /opt/dpdash/dpdash/get_accounts.sh tbillah

check_null(){

    # check for nullity in server down situation
    if [[ `tail -n 1 $1` == *"code 1" ]]
    then
        exit
    fi
}

cd /opt/dpdash/dpdash
source singularity/.env
prefix=dpdash_users_$(date +"%Y%m%d")

echo Name,Username,Email > users/$prefix.csv

/root/mongodb-linux-x86_64-rhel70-4.4.6/bin/mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdmongo?authSource=admin --eval "db.users.find().forEach(u=>print(u.display_name+','+u.uid+','+u.mail))" | tail -n +5 >> users/$prefix.csv

check_null users/$prefix.csv

for to in $@
do
    echo '' | mailx -s $prefix -a users/$prefix.txt -r tbillah@partners.org -- $to@mgb.org
done


# generate list of new registrants

current_list=users/dpdash_users_$(date +"%Y%m%d").csv
past_list=`ls users/dpdash_users_*.csv | tail -n 2 | head -n 1`

check_null $past_list

current_number=`cat $current_list | wc -l`
past_number=`cat $past_list | wc -l`

if [ $current_number -gt $past_number ]
then
    ind=$(( past_number+1 ))
    notify=1
fi

if [ ! -z $notify ]
then
    for to in $@
    do
        # sed -n ${ind},${current_number}p $current_list

        sed -n ${ind},${current_number}p $current_list | mailx -s "New DPdash registrants: verify their NDA DUC" -r tbillah@partners.org -- $to@mgb.org

    done
fi


