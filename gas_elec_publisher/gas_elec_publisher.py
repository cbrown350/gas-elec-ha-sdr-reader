#!/usr/bin/python3
 
import subprocess
import signal
import sys
import os
from pathlib import Path
import time
import pytz
from datetime import datetime
import paho.mqtt.publish as publish
import gas_elec_publisher.settings as settings
import json
import traceback
import logging
import gas_elec_publisher.mqtt_config as ha
import importlib.metadata

__version__ = importlib.metadata.version('gas-elec-ha-sdr-reader')

SW_VERSION = __version__
VENDOR_NAME = "cbrown350"
VENDOR_ID = "io-github-cbrown350"
REPO = "https://github.com/cbrown350/gas-elec-ha-sdr-reader"
DEVICE_ID = "gas_elec_publisher"
SERIAL_NUM_FILE = '/app/data/serial_num.txt'

TZ = os.getenv('TZ') or (settings.TZ if hasattr(settings, 'TZ') else 'UTC')
logging.Formatter.converter = lambda *args: datetime.now(tz=pytz.timezone(TZ)).timetuple()
FORMAT = '%(asctime)s %(message)s'
LOG_LEVEL = os.getenv('LOG_LEVEL') or settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else 'INFO'
numeric_log_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_log_level, int):
    logging.error('Invalid log level: %s' % LOG_LEVEL)
else:
    logging.basicConfig(encoding='utf-8', level=numeric_log_level, format=FORMAT)
logging.info(f"Set Log Level: {LOG_LEVEL}")
logging.info(f"Timezone: {TZ}")

logging.info(f"SW_VERSION: {SW_VERSION}")


SERIAL_NUM = os.getenv('SERIAL_NUM') if os.getenv('SERIAL_NUM') else settings.SERIAL_NUM if hasattr(settings, 'SERIAL_NUM') else None
if SERIAL_NUM:
    logging.info(f"Using serial number from env or settings.py: {SERIAL_NUM}")
else:
    logging.info("No SERIAL_NUM defined in settings.py or env")
    # get serial number from serial_num.txt and if empty or no file exists, create one from timestamp
    try:   
        with open(SERIAL_NUM_FILE, 'r') as f:
            SERIAL_NUM = f.read()
            logging.info(f'Using serial number from file: "{SERIAL_NUM}" (delete file to generate new serial number)')
        if not SERIAL_NUM:
            raise ValueError
    except FileNotFoundError or ValueError:
        filename = Path(SERIAL_NUM_FILE)
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.touch(exist_ok=True)
        with open(filename, 'w+') as f:
            SERIAL_NUM = datetime.now().strftime("%Y%m%d%H%M%S")
            f.write(SERIAL_NUM)
        logging.info(f'Using newly created serial number "{SERIAL_NUM}" stored in {SERIAL_NUM_FILE}')
UNIQUE_ID = f"{VENDOR_ID}_{DEVICE_ID}_{SERIAL_NUM}"

WATCHED_METERS = []
try:
    WATCHED_METERS = os.getenv("WATCHED_METERS") if os.getenv("WATCHED_METERS") \
            else settings.WATCHED_METERS if settings.WATCHED_METERS \
            else sys.exit("No WATCHED_METERS defined in settings.py or env")
    logging.info(f"Monitoring WATCHED_METERS: \n{WATCHED_METERS}")
    WATCHED_METERS = json.loads(WATCHED_METERS)
except json.decoder.JSONDecodeError:
    sys.exit("WATCHED_METERS is not valid JSON")
    
MQTT_HOST = os.getenv('MQTT_HOST') or settings.MQTT_HOST if hasattr(settings, 'MQTT_HOST') else sys.exit("No MQTT_HOST defined in settings.py or env")
MQTT_PORT = os.getenv('MQTT_PORT') or settings.MQTT_PORT if hasattr(settings, 'MQTT_PORT') else 1883
MQTT_USER = os.getenv('MQTT_USER') or settings.MQTT_USER if hasattr(settings, 'MQTT_USER') else None
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD') or settings.MQTT_PASSWORD if hasattr(settings, 'MQTT_PASSWORD') else None
RTL_TCP = os.getenv('RTL_TCP') or settings.RTL_TCP if hasattr(settings, 'RTL_TCP') else sys.exit("No RTL_TCP defined in settings.py or env")
RTL_MUX = os.getenv('RTL_MUX') or settings.RTL_MUX if hasattr(settings, 'RTL_MUX') else sys.exit("No RTL_MUX defined in settings.py or env")
RTLAMR = os.getenv('RTLAMR') or settings.RTLAMR if hasattr(settings, 'RTLAMR') else sys.exit("No RTLAMR defined in settings.py or env")


def shutdown(signum, frame):
    subprocess.call('/usr/bin/pkill -9 rtlamr', shell=True)
    subprocess.call('/usr/bin/pkill -9 rtl_mux', shell=True)
    subprocess.call('/usr/bin/pkill -9 rtl_tcp', shell=True)
    
    try:
        for meter in WATCHED_METERS:
            publish.single(topic=ha.AVAILABLE_TOPIC.format(VENDOR_ID=VENDOR_ID, meter_type=meter['type']), 
                        payload='offline', qos=1, hostname=MQTT_HOST, port=int(MQTT_PORT), auth=auth, retain=True)
    except Exception as ex:
        logging.error(f"MQTT Publish offline Failed: {str(ex)}")
        
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


auth = None
if len(MQTT_USER) and len(MQTT_PASSWORD):
        auth = {'username':MQTT_USER, 'password':MQTT_PASSWORD}
        
def send_mqtt_config():
    while True:
        try:
            for meter in WATCHED_METERS:
                logging.info(f"Sending MQTT Config for meter {meter['id']}")
                publish.single(topic=ha.HA_CONFIG_TOPIC_ENERGY.format(UNIQUE_ID=UNIQUE_ID, meter_type=meter['type'], meter_id=meter['id']), 
                               payload=ha.HA_CONFIG_PAYLOAD_ENERGY.format(STATE_TOPIC=ha.STATE_TOPIC.format(VENDOR_ID=VENDOR_ID, 
                                                                                                      meter_type=meter['type'], 
                                                                                                      meter_id=meter['id']), 
                                                                        AVAILABLE_TOPIC=ha.AVAILABLE_TOPIC.format(VENDOR_ID=VENDOR_ID,meter_type=meter['type']),
                                                                        VENDOR_NAME=VENDOR_NAME, SW_VERSION=SW_VERSION, REPO=REPO,
                                                                        VENDOR_ID=VENDOR_ID, DEVICE_ID=DEVICE_ID, UNIQUE_ID=UNIQUE_ID,
                                                                        meter_type_CAP=str(meter['type']).capitalize(),
                                                                        meter_type=meter['type'], meter_id=meter['id'], meter_units=meter['unit'], meter_icon=meter['icon'], meter_device_class=meter['device_class']), 
                               qos=1, hostname=MQTT_HOST, port=int(MQTT_PORT), auth=auth, retain=True)
                publish.single(topic=ha.HA_CONFIG_TOPIC_LINKQUALITY.format(UNIQUE_ID=UNIQUE_ID, meter_type=meter['type'], meter_id=meter['id']), 
                               payload=ha.HA_CONFIG_PAYLOAD_LINKQUALITY.format(STATE_TOPIC=ha.STATE_TOPIC.format(VENDOR_ID=VENDOR_ID, 
                                                                                                           meter_type=meter['type'], meter_id=meter['id']), 
                                                                            AVAILABLE_TOPIC=ha.AVAILABLE_TOPIC.format(VENDOR_ID=VENDOR_ID,meter_type=meter['type']),
                                                                            VENDOR_NAME=VENDOR_NAME, SW_VERSION=SW_VERSION, REPO=REPO,
                                                                            VENDOR_ID=VENDOR_ID, DEVICE_ID=DEVICE_ID, UNIQUE_ID=UNIQUE_ID,
                                                                            meter_type_CAP=str(meter['type']).capitalize(),
                                                                            meter_type=meter['type'], meter_id=meter['id']), 
                               qos=1, hostname=MQTT_HOST, port=int(MQTT_PORT), auth=auth, retain=True)
                publish.single(topic=ha.HA_CONFIG_TOPIC_LASTSEEN.format(UNIQUE_ID=UNIQUE_ID, meter_type=meter['type'], meter_id=meter['id']), 
                               payload=ha.HA_CONFIG_PAYLOAD_LASTSEEN.format(STATE_TOPIC=ha.STATE_TOPIC.format(VENDOR_ID=VENDOR_ID, 
                                                                                                        meter_type=meter['type'], meter_id=meter['id']), 
                                                                        AVAILABLE_TOPIC=ha.AVAILABLE_TOPIC.format(VENDOR_ID=VENDOR_ID,meter_type=meter['type']),
                                                                        VENDOR_NAME=VENDOR_NAME, SW_VERSION=SW_VERSION, REPO=REPO,
                                                                        VENDOR_ID=VENDOR_ID, DEVICE_ID=DEVICE_ID, UNIQUE_ID=UNIQUE_ID,
                                                                        meter_type_CAP=str(meter['type']).capitalize(),
                                                                        meter_type=meter['type'], meter_id=meter['id']), 
                               qos=1, hostname=MQTT_HOST, port=int(MQTT_PORT), auth=auth, retain=True)
                publish.single(topic=ha.AVAILABLE_TOPIC.format(VENDOR_ID=VENDOR_ID, meter_type=meter['type']), 
                               payload='online', qos=1, hostname=MQTT_HOST, port=int(MQTT_PORT), auth=auth, retain=True)
            break
        except Exception as ex:
            logging.error(f"MQTT Config Publish Failed: {str(ex)}")
            time.sleep(5)       

def publish_mqtt(topic, payload,):
    try:
        publish.single(topic, payload=payload, qos=1, hostname=MQTT_HOST, port=int(MQTT_PORT), auth=auth)
    except Exception as ex:
        logging.error(f"MQTT Publish Failed: {str(ex)}, will try to reconnect to MQTT server...")
        send_mqtt_config()

def start_rtltcp():
    global rtltcp
    rtltcp = subprocess.Popen([f"{RTL_TCP}"], shell=True, #  > /dev/null 2>&1 &
        stdin=None, stdout=None, stderr=subprocess.PIPE, close_fds=True)
    logging.info("Started rtl_tcp")
    
def start_rtlmux():    
    global rtlmux
    rtlmux = subprocess.Popen([f"{RTL_MUX}"], shell=True,
        stdin=None, stdout=None, stderr=subprocess.PIPE, close_fds=True)
    logging.info("Started rtl_mux")

def start_rtlamr():
    global rtlamr
    rtlamr = subprocess.Popen([f"{RTLAMR}"], stdout=subprocess.PIPE, shell=True, # 2> /dev/null
        stdin=None, stderr=subprocess.PIPE, close_fds=True)
    logging.info("Started rtlamr")

def main():
    send_mqtt_config()
    start_rtltcp()
    time.sleep(2)
    start_rtlmux()    
    time.sleep(2)
    start_rtlamr()
    time.sleep(2)

    while True:
        rtlamr_err = None
        try:
            amrline = rtlamr.stdout.readline().strip().decode()
            # amrline,rtlamr_err=rtlamr.communicate()
            # amrline = amrline.strip().decode()
            
            logging.debug(f"Received json: {amrline}")

            if not amrline:
                raise ValueError("No data received from rtlamr")
            
            data = json.loads(amrline)
            rtlamr.stderr.flush() # clear any error streams since just messages if json was valid
            if 'Message' not in data:
                logging.debug("Received amr data, but no Message key found")
                continue
            msg = data['Message']
            
            for meter in WATCHED_METERS:
                if meter['rtlsdr_id_name'] in msg and meter['rtlsdr_value_name'] in msg:
                    meter_id = msg[meter['rtlsdr_id_name']]
                    if str(meter_id) != meter['id']:
                        continue
                    current_reading = msg[meter['rtlsdr_value_name']]
                    meter_type = meter['type']
                    meter_units = meter['unit']
                    multiplier = meter['unit_multiplier']
                    
                    linkquality_val = 'unknown'
                    try:
                        linkquality = subprocess.Popen('/bin/cat /proc/net/wireless | tail -n -1 | tr -s - | cut -d" " -f 8',
                                                        shell=True,stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
                        output,err=linkquality.communicate()
                        if output:
                            linkquality_val = int(output.decode().strip().replace('.', ''))
                    except Exception:
                        logging.error('Error getting linkquality')
                        logging.error(traceback.format_exc())
                        
                    publish_mqtt(ha.STATE_TOPIC.format(VENDOR_ID=VENDOR_ID, meter_type=meter_type, meter_id=meter_id), 
                                payload=json.dumps({
                                    'energy': round(current_reading * multiplier, 6),
                                    'linkquality': linkquality_val,
                                    'last_seen': data['Time']
                                    }))
                    
                    logging.debug(f"Published topic, meter {meter_id} reading: {current_reading}")   
                    break
            
        except Exception:
            logging.error(traceback.format_exc())
            time.sleep(2)
            if rtltcp.poll() is not None:
                if rtltcp.stderr.readable():
                    _,err = rtltcp.communicate()
                    if err:
                        logging.error(f"rtl_tcp exited with error: {err.strip().decode()}")
                logging.error("rtl_tcp was not running, restarting...")
                start_rtltcp()
                time.sleep(3)
            if rtlmux.poll() is not None:
                if rtlmux.stderr.readable():
                    _,err = rtlmux.communicate()
                    if err:
                        logging.error(f"rtl_tcp exited with error: {err.strip().decode()}")
                logging.error("rtl_mux was not running, restarting...")
                start_rtlmux()
                time.sleep(3)
            if rtlamr.poll() is not None:
                if rtlamr.stderr.readable():
                    logging.error(f"rtlamr exited with error: {rtlamr.stderr.read().strip().decode()}")
                logging.error("rtlamr was not running, restarting...")
                start_rtlamr()
                time.sleep(3)
                

if __name__ == '__main__':
    main()                