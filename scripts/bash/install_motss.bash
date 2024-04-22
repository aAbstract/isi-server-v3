#!/bin/bash

echo "Installing motion streaming software"
apt update
apt install motion 

echo "Configuring motion service"
mkdir /var/log/motion
chmod 777 /var/log/motion
systemctl start motion
systemctl enable motion

echo "Adding motion service networking configs"
echo "webcontrol_localhost off" >> /etc/motion/motion.conf
echo "stream_localhost off" >> /etc/motion/motion.conf
systemctl restart motion

echo "Done"
