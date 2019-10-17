#!/bin/bash

# Wait for database to start
until $(nc -z db 3306); do { printf '.'; sleep 1; }; done
# Start Kamailio
/usr/sbin/kamailio -DD -E