
STATE_TOPIC = "{VENDOR_ID}/main_{meter_type}_meter_reader_{meter_id}"
AVAILABLE_TOPIC = "{VENDOR_ID}/{DEVICE_ID}_{SERIAL_NUM}/availability"

HA_CONFIG_TOPIC_ENERGY = "homeassistant/sensor/{UNIQUE_ID}/{meter_type}_{meter_id}_energy/config"
HA_CONFIG_PAYLOAD_ENERGY = '''
    {{
        "availability":
            [ 
                {{
                    "topic": "{AVAILABLE_TOPIC}"
                }} 
            ],
            "availability_mode": "all",
            "device":
                {{
                    "identifiers": [ "{UNIQUE_ID}_{meter_type}" ],
                    "manufacturer": "{VENDOR_NAME}",
                    "model": "RTL SDR wireless electrical power and gas company meter reader ({DEVICE_ID})",
                    "name": "Main {meter_type_CAP} Meter Reader",
                    "sw_version": "{SW_VERSION}"
                }},
            "device_class": "{meter_device_class}",
            "icon": "{meter_icon}",
            "enabled_by_default": true,
            "object_id": "main_{meter_type}_meter_energy",
            "origin":
                {{
                    "name": "{VENDOR_ID}",
                    "sw": "{SW_VERSION}",
                    "url": "{REPO}"
                }},
            "state_class": "total_increasing",
            "state_topic": "{STATE_TOPIC}",
            "unique_id": "{UNIQUE_ID}_{meter_type}_energy",
            "unit_of_measurement": "{meter_units}",
            "value_template": "{{{{ value_json.energy }}}}"}}
    '''

HA_CONFIG_TOPIC_LINKQUALITY = "homeassistant/sensor/{UNIQUE_ID}/{meter_type}_{meter_id}_linkquality/config"
HA_CONFIG_PAYLOAD_LINKQUALITY = '''
    {{
        "availability":
            [ 
                {{
                    "topic": "{AVAILABLE_TOPIC}"
                }} 
            ],
            "availability_mode": "all",
            "device":
                {{
                    "identifiers": [ "{UNIQUE_ID}_{meter_type}" ],
                    "manufacturer": "{VENDOR_NAME}",
                    "model": "RTL SDR wireless electrical power and gas company meter reader ({DEVICE_ID})",
                    "name": "Main {meter_type_CAP} Meter Reader",
                    "sw_version": "{SW_VERSION}"
                }},
            "enabled_by_default": true,
            "entity_category": "diagnostic",
            "icon": "mdi:signal",
            "name": "Linkquality",
            "object_id": "main_{meter_type}_meter_linkquality",
            "origin":
                {{
                    "name": "{VENDOR_ID}",
                    "sw": "{SW_VERSION}",
                    "url": "{REPO}"
                }},
            "state_class": "measurement",
            "state_topic": "{STATE_TOPIC}",
            "unique_id": "{UNIQUE_ID}_{meter_type}_linkquality",
            "unit_of_measurement": "dBm",
            "value_template": "{{{{ value_json.linkquality }}}}"}}
    '''

HA_CONFIG_TOPIC_LASTSEEN = "homeassistant/sensor/{UNIQUE_ID}/{meter_type}_{meter_id}_last_seen/config"
HA_CONFIG_PAYLOAD_LASTSEEN = '''
    {{
        "availability":
            [ 
                {{
                    "topic": "{AVAILABLE_TOPIC}"
                }} 
            ],
            "availability_mode": "all",
            "device":
                {{
                    "identifiers": [ "{UNIQUE_ID}_{meter_type}" ],
                    "manufacturer": "{VENDOR_NAME}",
                    "model": "RTL SDR wireless electrical power and gas company meter reader ({DEVICE_ID})",
                    "name": "Main {meter_type_CAP} Meter Reader",
                    "sw_version": "{SW_VERSION}"
                }},
            "device_class": "timestamp",
            "enabled_by_default": false,
            "entity_category": "diagnostic",
            "icon": "mdi:clock",
            "name": "Last seen",
            "object_id": "main_{meter_type}_meter_last_seen",
            "origin":
                {{
                    "name": "{VENDOR_ID}",
                    "sw": "{SW_VERSION}",
                    "url": "{REPO}"
                }},
            "state_topic": "{STATE_TOPIC}",
            "unique_id": "{UNIQUE_ID}_{meter_type}_last_seen",
            "value_template": "{{{{ value_json.last_seen }}}}"}}
    '''
