
#!/bin/sh

cp -n /etc/kamailio/dbtext/* /opt

/usr/sbin/kamailio -DD -E -m 1024 -M 256