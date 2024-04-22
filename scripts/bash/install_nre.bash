#!/bin/bash

echo "Installing NodeRED engine"
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
systemctl status nodered.service
node-red-start

username=isi_nr_admin
password=5JQ3bhmCSTe88aP4cwAgUUXDowss6L3JvQyDTPqhiyPZBDEd5yNNiBVFLSMYjJAG

echo "Configure these settings in ~/.nodered/settings.json file"
echo "adminAuth.users username: $username"
echo "adminAuth.users passowrd:"
echo "$password" | node-red admin hash-pw
