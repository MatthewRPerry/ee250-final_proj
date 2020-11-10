import time
import sys
import paho.mqtt.client as mqtt

sys.path.append('../../Software/Python/')
fan = False
water = False

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))

    #subscribe to temp data
    client.subscribe("perrymat/temp")
    client.message_callback_add("perrymat/temp", temp_callback)

    #subscribe to humidity data
    client.subscribe("perrymat/humidity")
    client.message_callback_add("perrymat/humidity", hum_callback)

    #subscribe to fan control
    client.subscribe("perrymat/fan_control")
    client.message_callback_add("perrymat/fan_control", fan_callback)

    #subscribe to water control
    client.subscribe("perrymat/water_control")
    client.message_callback_add("perrymat/water_control", water_callback)

#temp callback function
def temp_callback(client, userdata, message):
    temp = float(message.payload)
    print("Temp: "+ str(temp))
    if temp > 24 and fan == False:
        print("TOO HOT! Turn on fan!")
    elif temp < 21 and fan == True:
        print("TOO COLD! Turn off fan!")
    

#humidity callback
def hum_callback(client, userdata, message):
    hum = float(message.payload)
    print("Humidity: "+ str(hum))
    if hum > 80 and water == True:
        print("TOO HUMID! Turn off water!")
    elif hum < 70 and water == False:
        print("TOO DRY! Turn on water!")

def fan_callback(client, userdata, message):
    control = str(message.payload, "utf-8")
    print(control)
    if control == "FAN_ON":
        fan = True
    elif control == "FAN_OFF":
        fan = False

def water_callback(client, userdata, message):
    control = str(message.payload, "utf-8")
    print(control)
    if control == "WATER_ON":
        water = True
    elif control == "WATER_OFF":
        water = False


#Default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#handle user input
def handle_input(command):
    if command == "WATER_ON":
        client.publish("perrymat/water_control", "WATER_ON")
        water = True
    elif command == "WATER_OFF":
        client.publish("perrymat/water_control", "WATER_OFF")
        water = False
    elif command == "FAN_ON":
        client.publish("perrymat/fan_control", "FAN_ON")
        fan = True
    elif command == "FAN_OFF":
        client.publish("perrymat/fan_control", "FAN_OFF")
        fan = False

if __name__ == '__main__':

    #MQTT client/server setup
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="192.168.4.32", port=3000, keepalive=60)
    client.loop_start()

    print("Input Commands: WATER_ON, WATER_OFF, FAN_ON, FAN_OFF")

    while True:
        try:
            control_message = input()
            handle_input(control_message)
        
        except KeyboardInterrupt:
            print("Shutting down controller")
            break
            