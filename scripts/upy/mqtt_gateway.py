# web_repl_port: 8266
# web_repl_pass: 12345678

import json
import network
import webrepl

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print('Connecting to WiFi...')
wlan.connect('3ES', 'E$l@M2710900..')
print('Connected to WiFi')
print(wlan.ifconfig())


def send_test_payload(retain: bool):
    print(json.dumps({
        'topic': 'test_vspi_topic',
        'payload': 'test_vspi_msg',
        'retain': retain,
    }))


print('MQTT Gateway Ready')
webrepl.start()
