#!/bin/bash

if [ $# -lt 1 ] || [ $1 == '-h' ] || [ $1 == '--help' ]
then
    echo Usage: $0 /data/pnl/ tbillah sbouix jtbaker
    exit
fi


# obtain the second line of df output
__size=`df -HP $1 | tail -n 1`

# split it by space to obtain percentage field
IFS=' ' read -ra _size <<< "$__size"
_size=${_size[4]}

# remove the % character to convert to integer
size=${_size//%}

# notify if needed
if [ $size -gt 89 ]
then
    # df -HP /data/predict1/

    for r in ${@:2}
    do
        df -HP $1 | mailx -s "$1 reaching maximum" \
        -r tbillah@partners.org -- ${r}@partners.org
    done
fi


