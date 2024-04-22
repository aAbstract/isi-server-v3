#!/bin/bash

HTTP_STATUS=$(curl -I -s -o /dev/null "http://192.168.122.17:1880/api/$1" --write-out "%{http_code}")
if [ "$HTTP_STATUS" -eq 404 ]; then
    echo "HTTP route returned a 404 error."
else
    echo "HTTP route is available."
fi
