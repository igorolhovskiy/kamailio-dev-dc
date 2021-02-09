#!/bin/bash

if [[ "${ROLE}" == "UAS" ]]; then
    /usr/bin/sipp -sf /opt/sipp_uas.xml -m 100
else
# This is UAC
    while true; do
        echo -n "This is a loop for keeping container alive"
        date
        sleep 10
    done
fi