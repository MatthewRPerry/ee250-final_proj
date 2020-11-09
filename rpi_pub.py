"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys

sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+ str(rc))

#Default message callback. Please use custom callbacks.
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
    
    sensor_port = 2
    sensor_type = 0

    # #MQTT client/server setup
    # client = mqtt.Client()
    # client.on_message = on_message
    # client.on_connect = on_connect
    # #TODO: host ip and port
    # client.connect(host="127.0.0.1", port=3000, keepalive=60)
    # client.loop_start()

    temps = []
    hums = []

    while True:
        
        try:
        
            #read temp/humidity values
            [temp, humidity] = grovepi.dht(sensor_port, sensor_type)

            #filter results
            temp = lowpass(temp, temps)
            humidity = lowpass(humidity, hums)

            #publish values
            # client.publish("perrymat/temp", temp)
            # client.publish("perrymat/humidity", humidity)
            print("temp: " + str(temp) + " hum: " + str(humidity))

            #sleep
            time.sleep(1)
        
        except KeyboardInterrupt:
            print("Shutting down sensor")
            break
            