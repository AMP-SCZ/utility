#!/usr/bin/env bash

# do not change the base name
# mriqc-combined-mriqc-day1to9999.csv
# base hash
# 8d051eccc2a98eb4303bc62316124890ed47810c61ccde18b9d772e3ac379543

state=/opt/dpdash/dpstate

# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdata?authSource=admin --eval "db[\"8d051eccc2a98eb4303bc62316124890ed47810c61ccde18b9d772e3ac379543\"].remove({})"
echo ''

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdata?authSource=admin --eval "db.toc.remove({"study":\"mriqc\"})"
echo ''

# import new data
source /opt/dpdash/miniconda3/bin/activate
cd /data/predict/kcho/flow_test
import.py -c /opt/dpdash/dpimport/examples/config.yml MRI_ROOT/derivatives/quick_qc/mriqc-combined-mriqc-day1to9999.csv
