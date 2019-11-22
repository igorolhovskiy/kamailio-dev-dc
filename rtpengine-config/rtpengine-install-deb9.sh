#!/bin/bash

apt-get update

wget https://deb.sipwise.com/spce/mr7.5.1/pool/main/b/bcg729/libbcg729-0_1.0.4+git20180222-0.1~bpo10+1_amd64.deb
dpkg -i libbcg729-0_1.0.4+git20180222-0.1~bpo10+1_amd64.deb

wget https://deb.sipwise.com/spce/mr7.4.2/pool/main/n/ngcp-rtpengine/ngcp-rtpengine-daemon_7.4.2.2+0~mr7.4.2.2_amd64.deb
dpkg -i ngcp-rtpengine-daemon_7.4.2.2+0~mr7.4.2.2_amd64.deb
apt-get install -f -y

wget https://deb.sipwise.com/spce/mr7.4.2/pool/main/n/ngcp-rtpengine/ngcp-rtpengine-recording-daemon_7.4.2.2+0~mr7.4.2.2_amd64.deb
dpkg -i ngcp-rtpengine-recording-daemon_7.4.2.2+0~mr7.4.2.2_amd64.deb
apt-get install -f -y

wget https://deb.sipwise.com/spce/mr7.4.2/pool/main/n/ngcp-rtpengine/ngcp-rtpengine-utils_7.4.2.2+0~mr7.4.2.2_all.deb
dpkg -i ngcp-rtpengine-utils_7.4.2.2+0~mr7.4.2.2_all.deb
apt-get install -f -y

wget https://deb.sipwise.com/spce/mr7.4.2/pool/main/n/ngcp-rtpengine/ngcp-rtpengine-iptables_7.4.2.2+0~mr7.4.2.2_amd64.deb
dpkg -i ngcp-rtpengine-iptables_7.4.2.2+0~mr7.4.2.2_amd64.deb
apt-get install -f -y

wget https://deb.sipwise.com/spce/mr7.4.2/pool/main/n/ngcp-rtpengine/ngcp-rtpengine-kernel-dkms_7.4.2.2+0~mr7.4.2.2_all.deb
dpkg -i ngcp-rtpengine-kernel-dkms_7.4.2.2+0~mr7.4.2.2_all.deb
apt-get install -f -y

wget https://deb.sipwise.com/spce/mr7.4.2/pool/main/n/ngcp-rtpengine/ngcp-rtpengine_7.4.2.2+0~mr7.4.2.2_all.deb
dpkg -i ngcp-rtpengine_7.4.2.2+0~mr7.4.2.2_all.deb
apt-get install -f -y