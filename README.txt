Matthew Perry
4354903663

demo video:

Compilation:
rpi.py must be run on the the raspberry pi with the appropriate sensors.
control.py should be run in terminal.
In both programs, mqtt_IP and influx_IP (and ports) must be set to the correct values before compiling.
An MQTT broker and influxdb server must be running before compiling the programs.

Libraries:
paho-mqtt
influxdb-python

moquitto was used as the mqtt broker
influxdb was used as the server