#!/bin/bash

# install deps
pip install "fastapi[all]"
pip install paho-mqtt
pip install opencv-python
sudo apt install cmake
pip install face_recognition

sudo echo "#User Settings" >> /etc/sudoers
sudo echo "%sudo ALL=NOPASSWD: /bin/systemctl start isi_surveillance_server.service" >> /etc/sudoers
