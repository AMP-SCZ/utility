# utility

This repository is the storehouse of all DPdash utility scripts. Currently, it consists of scripts that make DPdash importable files.

---

* `remove_collections.js`

> /data/predict/utility/gen_hash.py  /path/to/YA_metadata.csv mriqc > /tmp/mriqc_hashes.txt

> mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@\`hostname\`:27017/dpdata?authSource=admin --eval "hash_script=\\"/tmp/mriqc_hashes.txt\\"" /data/predict/utility/remove_collections.js

(The back slashes are important: `\"/tmp/mriqc_hashes.txt\"`



* `remove_studies.js`

> mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@\`hostname\`:27017/dpdata?authSource=admin /data/predict/utility/remove_studies.js


---

The mechanism for downloading configuration item at server backend is described in [this](https://github.com/AMP-SCZ/dpdash/wiki/Download-configuration) wiki.
