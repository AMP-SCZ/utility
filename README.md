[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7849718.svg)](https://doi.org/10.5281/zenodo.7849718)

Please cite this repository in AMP® SCZ papers as:

Billah T, Cho KIK, Nicholas S, Mohandass D, Ennis M, Eichi HR, Bouix S, Baker JT, *Accelerating Medicines Partnership® Schizophrenia (AMP® SCZ) Data Processing and Submission Software*, https://github.com/AMP-SCZ/utility, 2022, DOI: 10.5281/zenodo.7849718

# utility

This repository is the storehouse of all DPdash utility scripts. Currently, it consists of scripts that make DPdash importable files.


### Install

Prerequisites are only Python libraries. Install them against Python 3 as:

> pip install -r requirements.txt

https://github.com/AMP-SCZ/dpimport and https://github.com/NDAR/nda-tools
are two packages used by several programs in this repository.
They are put in the *requirements.txt* too.

---

### Usage

Most scripts' usage can be obtained by `./script.* --help`.

Some scripts' usage can be obtained by `cat ./script.*`.

Only outstanding ones are noted below:


* `remove_collections.js`

> /data/predict/utility/gen_hash.py  /path/to/YA_metadata.csv mriqc > /tmp/mriqc_hashes.txt

> mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@\`hostname\`:27017/dpdata?authSource=admin --eval "hash_script=\\"/tmp/mriqc_hashes.txt\\"" /data/predict/utility/remove_collections.js

(The back slashes are important: `\"/tmp/mriqc_hashes.txt\"`



* `remove_studies.js`

> mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@\`hostname\`:27017/dpdata?authSource=admin /data/predict/utility/remove_studies.js


---

The mechanism for downloading configuration item at server backend is described in [this](https://github.com/AMP-SCZ/dpdash/wiki/Download-configuration) wiki.


### Selective PRESCIENT upload, download, shift

1. Populate `Prescient/PHOENIX/PROTECTED/rpms_records.txt` as:

```
PrescientCG/raw/CG12345/surveys
PrescientME/raw/ME12345/surveys
PrescientHK/raw/HK12345/surveys
...
...
```

2. Set `FORCE=1` in `utility/_rpms_to_redcap.sh`. Execute it as:

> _rpms_to_redcap.sh /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED /data/predict1/utility/yale-real 123456

It will use `rpms_records.txt`.

3. Clean duplicate arms if needed:

> clean_old_arm.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED 123456

4. Download the JSONs. `rpms_recods.txt` will be used to select JSONs.

> down_mgb_redcap_records.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ 123456 1 1

5. Shift the dates:

> for d in $(cat rpms_records.txt); do shift_redcap_dates.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ "$d/*.Prescient.json" /data/predict1/utility/yale-real/CloneOfYaleRealRecords_DataDictionary_2024-04-16.csv 1 1; done


Steps 3-5 basically imitates `utility/clean_down_shift.sh` but with the trailing `1` meant for force re-download and re-shift.

