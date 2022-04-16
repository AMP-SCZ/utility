#!/usr/bin/env bash

# do not change the base name
# mriqc-combined-mriqc-day1to9999.csv
# base hash
# 8d051eccc2a98eb4303bc62316124890ed47810c61ccde18b9d772e3ac379543

# dpstage.dipr
HOST=
PORT=
state=
MONGO_PASS=
CONFIG=

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin --eval "db[\"8d051eccc2a98eb4303bc62316124890ed47810c61ccde18b9d772e3ac379543\"].remove({})"
echo ''

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin --eval "db.toc.remove({"study":\"mriqc\"})"
echo ''

# import new data
source /data/pnl/soft/pnlpipe3/miniconda3/bin/activate && conda activate dpimport
cd /data/predict/kcho/flow_test
import.py -c /data/predict/dpimport/examples/$CONFIG MRI_ROOT/derivatives/quick_qc/mriqc-combined-mriqc-day1to9999.csv
