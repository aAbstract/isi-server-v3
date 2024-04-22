#!/bin/bash

# echo "Installing eclipse mosquitto broker"
# apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
# apt-get update
# apt install mosquitto

echo -e "\n# User Settings" >> /etc/mosquitto/mosquitto.conf
echo "Configuring mosquitto broker"
echo "per_listener_settings true" >> /etc/mosquitto/mosquitto.conf
echo "allow_anonymous false" >> /etc/mosquitto/mosquitto.conf

echo "Configuring username and password"
username=isi_muser
password=oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX
echo "$username:$password" > /etc/mosquitto/passwords
mosquitto_passwd -U /etc/mosquitto/passwords

echo "Configuring network"
echo "listener 1883" >> /etc/mosquitto/mosquitto.conf
echo "password_file /etc/mosquitto/passwords" >> /etc/mosquitto/mosquitto.conf
echo "listener 9001" >> /etc/mosquitto/mosquitto.conf
echo "protocol websockets" >> /etc/mosquitto/mosquitto.conf
echo "password_file /etc/mosquitto/passwords" >> /etc/mosquitto/mosquitto.conf

systemctl restart mosquitto.service
echo "Done"
