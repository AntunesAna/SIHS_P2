import random
import RPi.GPIO as gpio
from gpiozero import Servo
from time import sleep

from paho.mqtt import client as mqtt_client



broker = 'test.mosquitto.org'
port = 1883
topic = "UEA_SIHS/nadine"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

username = 'teste123'
password = 'sorvete'

message = 'none'

gpio.setmode(gpio.BCM)
gpio.setup(5, gpio.IN)
gpio.setup(6, gpio.OUT)
servo = Servo(17)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("MQTT Broker conectado! ;)")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global message
        print(msg.payload.decode())
        message = msg.payload.decode()
        
    client.subscribe(topic)
    client.on_message = on_message

    
def modulo(client: mqtt_client):
    global message
    while True:
        
        sleep(1)

        client.publish(topic,gpio.input(5))

        if(message == 'Ligada'):
            gpio.output(6, gpio.HIGH)
            

        if(message == 'Desligada'):
            gpio.output(6, gpio.LOW)
            
            
        if(message == 'Destrancada'):
            servo.value = -1
            
        if(message == 'Trancada'):
            servo.value = 1
        
      


def run():
    client = connect_mqtt()
    client.loop_start()
    #publish(client)
    subscribe(client)
    
    modulo(client)


if __name__ == '__main__':
    run()
