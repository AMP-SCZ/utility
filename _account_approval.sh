#!/bin/bash

# It is run within VM as root
# Usage:
# ./_account_approval.sh abc123@partners.org
# ./_account_approval.sh list.txt
# Where list.txt contains:
# abc123@partners.org
# def456@gmail.com
# ...

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
    -c sylvain.bouix@etsmtl.ca -c jtbaker@partners.org -c tkapur@partners.org -- $e
done


