### Steps to prepare data from NDA

1. Make API call:

```bash
cd /data/predict1/to_nda/nda-submissions/penncnb01/

DATA="token=${TOKEN}&content=report&format=json&report_id=&rawOrLabel=raw&rawOrLabelHeaders=raw&exportCheckboxLabel=false&returnFormat=csv"
curl -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      https://redcap.med.upenn.edu/api/ > downloaded.csv
```

2. Replace IDs with official AMP-SCZ IDs:

> /data/predict1/utility/nda-transform/_penncnb01.py /path/to/downloaded.csv replace


3. Ask Dheshan to filter upto a certain timepoint e.g. `month_2`


4. Shift dates:

> /data/predict1/utility/nda-transform/_penncnb01.py filtered.csv shift


5. Prepare data for NDA:

```
cd /data/predict1/to_nda/nda-submissions/network_combined
/data/predict1/utility/nda-transform/penncnb01.py --dict penncnb01 --root /data/predict1/data_from_nda/ -t"Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o penncnb01.csv --shared ndar_subject01.csv --data ../penncnb01/date_shifted_20240305.csv
```

6. Validate:

```
cd /data/predict1/utility/nda-transform
./submit.sh -f penncnb01
```

