import time
import sys
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb import InfluxDBClient

sys.path.append('../../Software/Python/')
import grovepi

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))

    #subscribe to fan
    client.subscribe("control/fan")
    client.message_callback_add("control/fan", fan_callback)

    #subscribe to water
    client.subscribe("control/water")
    client.message_callback_add("control/water", water_callback)

#fan callback function
def fan_callback(client, userdata, message):
    message = str(message.payload, "utf-8")
    if message == "FAN_ON":
        grovepi.digitalWrite(3,1)
    elif message == "FAN_OFF":
        grovepi.digitalWrite(3,0)

#water callback
def water_callback(client, userdata, message):
    message = str(message.payload, "utf-8")
    if message == "WATER_ON":
        grovepi.digitalWrite(4,1)
    elif message == "WATER_OFF":
        grovepi.digitalWrite(4,0)

#Default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#low pass filter: moving average(l=5)
def lowpass(val, arr):
    arr.append(val)
    l = len(arr)
    
    if l > 5:
        arr.pop(0)
        l=5
    
    val = 0
    for i in range(l):
        val += arr[i]
    
    return val/l

if __name__ == '__main__':
    mqtt_IP = "192.168.4.32"
    mqtt_port = 3000
    influx_IP = "192.168.4.32"
    influx_port = 8086

    influx_user = 'admin'
    influx_password = 'password'

    #MQTT client/server setup
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host=mqtt_IP, port=mqtt_port, keepalive=60)
    client.loop_start()

    #influx server
    client = InfluxDBClient(influx_IP, influx_port, influx_user, influx_password, 'final')
    client.create_database('final')
    
    sensor_port = 2
    sensor_type = 0

    temps = []
    hums = []


    while True:
        try:
            #read temp/humidity values
            [temp, humidity] = grovepi.dht(sensor_port, sensor_type)

            #filter results
            temp = lowpass(temp, temps)
            humidity = lowpass(humidity, hums)

            #load json
            dt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            data = [
                {
                    "measurement": "temp_humidity",
                    "tags": {
                        "host": "server01",
                        "region": "us-west"
                    },
                    "time": dt,
                    "fields": {
                        "temp": temp,
                        "humidity": humidity
                    }
                }
            ]

            #send to database
            client.write_points(data)

            #sleep
            time.sleep(1)
        
        except KeyboardInterrupt:
            print("Shutting down sensor")
            break
            