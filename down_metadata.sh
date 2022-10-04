#!/usr/bin/bash

# download this script
# cd && wget -O down_metadata.sh

# cron job at every midnight
# 0 0 * * * ~/down_metadata.sh

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
echo "" | mailx -s $pronet -a $pronet -r EMAIL -- tbillah@partners.org kcho@bwh.harvard.edu

