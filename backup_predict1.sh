#!/bin/bash

# Usage:
# /data/predict1/utility/backup_predict1.sh duply_profile_name

source /data/pnl/soft/pnlpipe3/duply_backup/env.sh

duply /data/predict1/duply_backup/duply_profile/$1 backup

