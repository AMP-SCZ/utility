#!/bin/bash

# running at predict VM
# 0 8 * * * /opt/dpdash/dpdash/get_accounts.sh tbillah

cd /opt/dpdash/dpdash
source singularity/.env
prefix=dpdash_users_$(date +"%Y%m%d")
/root/mongodb-linux-x86_64-rhel70-4.4.6/bin/mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdmongo?authSource=admin --eval "db.users.find().forEach(u=>print(u.display_name+','+u.uid+','+u.mail))" > users/$prefix.txt

for to in $@
do
    echo '' | mailx -s $prefix -a users/$prefix.txt -r tbillah@partners.org -- $to@partners.org
done

