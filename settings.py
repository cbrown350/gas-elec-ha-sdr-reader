MQTT_HOST = 'mosquitto' # dev container default
MQTT_PORT = 1883
MQTT_USER = 'mosquitto' # dev container default
MQTT_PASSWORD = 'mosquitto' # dev container default

LOG_LEVEL = 'DEBUG' # DEBUG, INFO, WARNING, ERROR, CRITICAL

# SERIAL_NUM = 'test'

WATCHED_METERS = '''
        [
          {
            "type": "elec",
            "unit": "kWh",
            "unit_multiplier": 0.01,
            "id": "20190118",
            "rtlsdr_id_name": "ERTSerialNumber",
            "rtlsdr_value_name": "LastConsumptionCount",
            "icon": "mdi:meter-electric",
            "device_class": "energy"
          }
        ]
        '''
# 2.8316846592 m³ = 1 ccf (ft³)
# $11.628 per Dth, 2.5 billed Dth per 2.8 used CCF (ft³) = $10.43821482 per CCF (ft³)
# $10.43821482 per CCF (ft³) / 2.8316846592 m³ = $3.66641914 per m³

# RTL_TCP = '/usr/bin/rtl_tcp -a 0.0.0.0 -p 1234'
RTL_TCP = '/bin/sh -c "while sleep 1000; do :; done"' # if not using local rtl_tcp, but using remote rtl_tcp

# RTL_MUX = '/usr/local/bin/rtlmux -h 127.0.0.1 -p 1234 -l 2222'
RTL_MUX = '/bin/sh -c "while sleep 1000; do :; done"' # if not using local rtlmux (remote server)

# RTLAMR = '/usr/local/bin/rtlamr -server=127.0.0.1:2222 -msgtype=scm+,idm --format=json' # local server
RTLAMR = '/usr/local/bin/rtlamr -server=192.168.2.193:2222 -msgtype=scm+,idm --format=json' # remote test server
# RTLAMR = 'echo \'{"Time":"2023-10-11T03:03:33.788020063Z","Offset":0,"Length":0,"Type":"IDM","Message":{"Preamble":1431639715,"PacketTypeID":28,"PacketLength":92,"HammingCode":198,"ApplicationVersion":4,"ERTType":7,"ERTSerialNumber":20190118,"ConsumptionIntervalCount":70,"ModuleProgrammingState":188,"TamperCounters":"AQEAMgUA","AsynchronousCounters":0,"PowerOutageFlags":"BAAAAAQA","LastConsumptionCount":2528113,"DifferentialConsumptionIntervals":[11,23,28,27,27,27,27,27,25,25,25,26,26,25,26,26,27,27,26,26,24,26,26,26,27,26,18,18,20,20,20,19,19,18,21,18,10,10,12,11,12,10,11,10,11,11,12],"TransmitTimeOffset":4498,"SerialNumberCRC":38882,"PacketCRC":64278}}\'' # test frame