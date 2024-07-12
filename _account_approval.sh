#!/bin/bash

if [ -z $1 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]
then
    echo """
It is run within VM as root
Usage:
$0 abc123@partners.org
$0 abc123@partners.org def456@gmail.com
$0 list.txt
Where list.txt contains:
abc123@partners.org
def456@gmail.org
...
"""
    exit
fi

source /opt/dpdash/dpdash/singularity/.env

# configure all registered accounts
# mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
# --tlsCertificateKeyFile $state/ssl/mongo_client.pem \
# mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdmongo?authSource=admin \
# /opt/dpdash/dpdash/_configure_account1.mongo.js


if [ -f $1 ]
then
    recepients=$(cat $1)
else
    recepients=$@
fi

for e in $recepients
do
    echo $e
    
    # configure one (selective) account at a time
    mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
    --tlsCertificateKeyFile $state/ssl/mongo_client.pem \
    mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdmongo?authSource=admin \
    --eval "user=\"$e\"" \
    /opt/dpdash/dpdash/_configure_account1.mongo.js

    cat account_approval.txt | mailx -s "DPdash account approved" -r tbillah@partners.org \
    -c sylvain.bouix@etsmtl.ca -c jtbaker@partners.org -c tkapur@partners.org \
    -c aasgari@partners.org -- $e

    echo
done

