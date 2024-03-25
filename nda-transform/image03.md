### Steps to prepare data for NDA


1. Obtain `.csv` file from Kevin

> /data/predict1/to_nda/nda-mri-test/*_upload/AMPSCZ_submission.csv

Softlink it in proper place:

```
cd nda-submissions/image03
ln -s ../../nda-mri-test/*_upload/AMPSCZ_submission.csv
```

2. Populate the mandatory columns using `image03.py`:

```bash
cd /data/predict1/to_nda/nda-submissions/network_combined/
/data/predict1/utility/nda-transform/image03.py --shared ndar_subject01.csv -o image03.csv --root /data/predict1/data_from_nda/ --template "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" --data ../image03/AMPSCZ_submission.csv --dict image03 --version 03
```

