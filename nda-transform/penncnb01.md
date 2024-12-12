### Steps to prepare data from NDA

1. Ask Sylvain to download all Penn CNB records from their REDCap in a CSV file.

   In theory, we should be able to do the above via an API call but it is not feasible as API call requires `redcap_id`
   which is different than AMPSCZ ID. And we do not know the former until the data reach us.

   <details><summary>Here is the theoretical API call:</summary>

      ```bash
      cd /data/predict1/to_nda/nda-submissions/penncnb01/
      
      TOKEN=123456
      DATA="token=${TOKEN}&content=report&format=json&report_id=&rawOrLabel=raw&rawOrLabelHeaders=raw&exportCheckboxLabel=false&returnFormat=csv"
      curl -H "Content-Type: application/x-www-form-urlencoded" \
            -H "Accept: application/json" \
            -X POST \
            -d $DATA \
            https://redcap.med.upenn.edu/api/ > downloaded.csv
      ```

    </details>
      
   [Here](https://github.com/AMP-SCZ/utility/blob/3db75901674d0467d6bfb5a6e3e92ae2d9e1ba82/down_mgb_redcap_records.py#L75) is a similar Python API call to MGB REDCap.

2. Replace IDs with official AMP-SCZ IDs:

> /data/predict1/utility/nda-transform/_penncnb01.py downloaded.csv replace


3. Ask Dheshan to filter up to a certain timepoint e.g. `month_2`


4. Shift dates:

> /data/predict1/utility/nda-transform/_penncnb01.py filtered.csv shift


5. Prepare data for NDA:

```
cd /data/predict1/to_nda/nda-submissions/network_combined
/data/predict1/utility/nda-transform/penncnb01.py --dict penncnb01 --root /data/predict1/data_from_nda/ -t "Pr*/PHOENIX/GENERAL/*/processed/*/surveys/*.Pr*.json" -o penncnb01.csv --shared ndar_subject01.csv --data ../penncnb01/date_shifted_20240305.csv
```

6. Validate:

```
cd /data/predict1/utility/nda-transform
./submit.sh -f penncnb01
```

