import time
import sys
import paho.mqtt.client as mqtt

sys.path.append('../../Software/Python/')

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))
    print()

#Default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#handle user input
def handle_input(command):
    if command == "WATER_ON":
        print("pub water on")
        client.publish("control/water", "WATER_ON")
    elif command == "WATER_OFF":
        print("pub water off")
        client.publish("control/water", "WATER_OFF")
    elif command == "FAN_ON":
        print("pub fan on")
        client.publish("control/fan", "FAN_ON")
    elif command == "FAN_OFF":
        print("pub fan off")
        client.publish("control/fan", "FAN_OFF")

if __name__ == '__main__':
    mqtt_IP = "192.168.4.32"
    mqtt_port = 3000
    #MQTT client/server setup
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host=mqtt_IP, port=mqtt_port, keepalive=60)
    client.loop_start()

    print("Input Commands: WATER_ON, WATER_OFF, FAN_ON, FAN_OFF")

    while True:
        try:
            control_message = input()
            handle_input(control_message)
        
        except KeyboardInterrupt:
            print("Shutting down controller")
            break