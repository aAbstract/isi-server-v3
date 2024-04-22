#!/bin/bash

alias e2e="python ./e2e/e2e_main.py"
alias mdswitch="python ./scripts/mqtt_device_switch.py main_switch_0"
alias mdplug="python ./scripts/mqtt_device_switch.py main_plug_4"
alias mddht="python ./scripts/mqtt_device_dht.py"
alias mdfl="python ./scripts/mqtt_device_fl_sec.py flood_sensor_7"
alias mdsl="python ./scripts/mqtt_device_fl_sec.py security_lock_6"
alias mdmot="python ./scripts/mqtt_device_motion.py"
alias e2e_login="e2e -m us_login -us us_login"
