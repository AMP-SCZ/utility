#!/bin/bash

# it is run within VM as root

source /opt/dpdash/dpdash/singularity/.env
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdmongo?authSource=admin \
/opt/dpdash/dpdash/_configure_account.mongo.js


if [ -f $1 ]
then
    recepients=$(cat $1)
else
    recepients=$1
fi

for e in $recepients
do
    echo $e
    cat account_approval.txt | mailx -s "DPdash account approved" -r tbillah@partners.org \
    -c sylvain.bouix@etsmtl.ca -c jtbaker@partners.org -- $e
done


