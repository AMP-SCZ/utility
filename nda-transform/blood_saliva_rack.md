This document outlines the steps for generating blood/saliva manifests:

1. Generate ndar_subject01

```
cd /data/predict1/utility/nda-transform/
./generate.sh -f ndar_subject01 -n Pronet
```

2. Generate combined `blood_saliva_rack_Pronet.csv`

> ./blood_saliva_rack.sh

3. Split combined file by rack code

> ./sort_blood_saliva_rack.sh -n Pronet -s NN -c "7000432740 3000714519 3000714520"

Split files are stored in `/data/predict1/to_nda/nda-submissions/fluid_shipment`
while previous split files are backed up to `fluid_shipment.${datestamp}` folder.

4. Go to `https://www.dropbox.com/home/Tashrif%20Billah/blood_saliva_manifests` and confirm
availability of the new manifests. If a manifest has not changed since last time it was
uploaded, it will not be re-uploaded. You can observe this subtlety by checking the
`Modified` column.
