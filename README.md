<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px alt=" " src="https://github.com/cbrown350/gas-elec-ha-sdr-reader/blob/master/gas-elec-ha-sdr-reader-logo.png?raw=true"></a>
</p>

<h3 align="center">gas-elec-ha-sdr-reader</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Python3 script to read gas and electric meters using a USB RTL-SDR dongle that runs on Docker and reports values to Home Assistant via MQTT.<br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
- [<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/list-check.svg" width="15" height="15"> Prerequisites](#prerequisites)
- [<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gears.svg" width="15" height="15"> Configuration](#configuration)

## 🧐 About <a name = "about"></a>

This project is written in python3 and uses rtlamr to read gas and electrical meters wirelessly using a USB RTL SDR dongle (I'm using a Nooelec RTL-SDR v5). It runs in a Docker container and reports the values to Home Assistant via MQTT. It heavily relies on the [rtl-sdr](https://osmocom.org/projects/rtl-sdr/wiki) and [rtlamr](https://github.com/bemasher/rtlamr) projects. Additionally, [rtlmux](https://github.com/slepp/rtlmux) is used to allow for outside control of the dongle if desired by managing network traffic between rtlamr and rtl-sdr, which communicates directly with the dongle. The script connects to rtlmux to watch for new meter readings and then publishes them to MQTT in a format Home Assistant recognizes as well as publishing an auto discovery message for each meter on startup. Various environment variables configure the MQTT connection, rtlamr, rtlmux, and rtl_sdr commands, meters to watch for and other settings outlined below.

## 🏁 Getting Started <a name = "getting_started"></a>

The quickest way to use this software is to download the docker-compose.yaml file, update it with your information and run it using docker-compose using the existing image (available for ARM and AMD64). You can also build the image yourself using the Dockerfile. If you are not using Docker, you can run the script directly using python3 and change configuration in the settings.py file.

1. Download the docker-compose.yaml file from the releases page or from the repository.
2. Update the docker-compose.yaml file with your MQTT broker information and other settings directly or in a new .env file.
3. Run the following command to start the container:
```
docker-compose up -d
```
4. Check the logs for any errors and to make sure it is running and receiving data (you'll see any meters in your area that are being read if you set logging level to 'DEBUG' instead of 'INFO'):
```
docker-compose logs -f
```

### <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/list-check.svg" width="15" height="15"> Prerequisites

This project only requires docker to be installed if you use the docker-compose file. If you are not using Docker, you will need to install the following dependencies:

- Python3
- rtl-sdr
- rtlamr
- rtlmux

See the Dockerfile for the commands to install these and any other dependencies.

### <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gears.svg" width="15" height="15"> Configuration
There are a few environment variables you can set to configure the program:

| Variable | Description | Default |
| :-------- | ----------- | ------- |
| MQTT_HOST | MQTT broker host | mosquitto |
| MQTT_PORT | MQTT broker port | 1883 |
| MQTT_USERNAME | MQTT broker username | mosquitto |
| MQTT_PASSWORD | MQTT broker password | mosquitto |
| LOGGING_LEVEL | logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | DEBUG |
| TZ | timezone | America/Denver |
| RTL_TCP | path to rtl_tcp binary and options | /usr/bin/rtl_tcp -a 127.0.0.1 -p 1234 |
| RTLMUX | path to rtlmux binary and options | /usr/local/bin/rtlmux -h 127.0.0.1 -p 1234 -l 2222 |
| RTLAMR | path to rtlamr binary and options | /usr/local/bin/rtlamr -server=127.0.0.1:2222 -msgtype=scm+,idm --format=json |
| WATCHED_METERS | list of meters to watch for (see docker-compose.yaml or settings.py for format in json) | (test values) |

When it initially starts, it will look for a serial number to use in the environment variables or in the settings.py file. If it doesn't find one, it will create one and store it in /app/data/serial_num.txt so it can be reused as a unique value for the MQTT topic. If you want to change the serial number, you can delete the file and it will create a new one on the next run.