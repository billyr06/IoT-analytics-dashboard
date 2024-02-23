import random
import time
import json
from paho.mqtt import client as mqtt_client

broker = 'mqtt.eclipseprojects.io'  # Using a public broker for demonstration
port = 1883
topic = "iot/simulator"
client_id = f'python-mqtt-{random.randint(0, 10000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code", rc)
        client.subscribe(topic)

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv311, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION1)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        temperature = round(random.uniform(20, 30), 2)
        humidity = round(random.uniform(30, 60), 2)
        light_level = random.randint(200, 800)
        message = json.dumps({
            'temperature': temperature,
            'humidity': humidity,
            'light_level': light_level
        })
        result = client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"Sent {message} to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(5)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()
