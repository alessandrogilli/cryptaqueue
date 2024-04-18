import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import argparse
import paho.mqtt.client as mqtt
from crypta import Crypta

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code} to {BROKER_ADDRESS}")
    print(f"Topic: {TOPIC}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    plaintext = cr.try_decrypt(msg.payload)
    if plaintext is not None:
        print(plaintext)
    else:
        print("received non message")

if __name__ == "__main__":

    load_dotenv()
    BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
    BROKER_PORT = int(os.getenv('BROKER_PORT'))

    cr = Crypta()

    parser = argparse.ArgumentParser(description='CryptaQueue Chat Viewer.')
    parser.add_argument('--channel', nargs='?', const='default', default=None, help='The channel to use.')

    args = parser.parse_args()

    channel = args.channel
    if channel is None:
        channel = "global"

    TOPIC = os.getenv('TOPIC')
    TOPIC = f"{TOPIC}/{channel}"

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    print(f"CryptaQueue.")

    try:
        mqttc.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    except:
        print("Connection error.")
        exit(-1)

    try:
        mqttc.loop_forever()
    except(KeyboardInterrupt):
        exit()




