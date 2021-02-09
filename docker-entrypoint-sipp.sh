#!/bin/sh

if [[ "${ROLE}" == "UAS" ]]; then
    /usr/bin/sipp -sf /opt/sipp_uas.xml -r 1 -l 1 -m 1
else
# This is UAC
    while true; do
        echo -n "This is a loop for keeping container alive"
        date
        sleep 10
    done
fi