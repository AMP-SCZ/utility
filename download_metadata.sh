#!/usr/bin/bash

# download this script
# cd && wget https://raw.githubusercontent.com/AMP-SCZ/utility/main/download_metadata.sh

# cron job at every midnight
# 0 0 * * * ~/download_metadata.sh

# create directory for archiving purpose
ARCHIVE=$HOME/yale_dict_archive
mkdir -p $ARCHIVE && cd $ARCHIVE

CURL=`which curl`
datestamp=$(date +"%Y%m%d")

# download blank data dictionary
pronet=pronet_dict_${datestamp}.csv
DATA="token=TOKEN&content=metadata&format=csv&returnFormat=json"
$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      https://redcap.research.yale.edu/redcap/api/ > $pronet

# email Tashrif and Kevin
# echo "" | mailx -s $pronet -a $pronet -r EMAIL -- tbillah@partners.org kcho@bwh.harvard.edu

# use dropbox as a vehicle instead
dbxcli put $pronet pronet_metadata/$pronet

