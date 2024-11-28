import argparse
import datetime
import json
import os

import paho.mqtt.publish as publish
from dotenv import load_dotenv

from colors import Colors
from crypta import Crypta


def send_message(msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plaintext_json = {
        "time": current_time,
        "usn": CHAT_USERNAME,
        "msg": msg,
    }
    if COLOR:
        plaintext_json["color"] = COLOR
    plaintext = json.dumps(plaintext_json)
    # plaintext = f"{current_time} - {CHAT_USERNAME}: {msg}"
    ciphertext = cr.encrypt(plaintext=plaintext)
    try:
        publish.single(TOPIC, ciphertext, hostname=BROKER_ADDRESS, port=BROKER_PORT)
    except:
        print("Connection error.")


if __name__ == "__main__":
    cr = Crypta()
    load_dotenv()
    BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")
    BROKER_PORT = int(os.getenv("BROKER_PORT"))
    TOPIC = os.getenv("TOPIC")

    CHAT_USERNAME = os.getenv("CHAT_USERNAME")
    if not CHAT_USERNAME:
        CHAT_USERNAME = os.popen("uname -n").read().rstrip("\n")

    COLOR = os.getenv("COLOR") or ""
    COLOR = getattr(Colors, COLOR, None)

    parser = argparse.ArgumentParser(description="CryptaQueue Chat Sender.")
    parser.add_argument(
        "--channel",
        nargs="?",
        const="default",
        default=None,
        help="The channel to use.",
    )
    parser.add_argument(
        "--direct",
        nargs="?",
        const="default",
        default=None,
        help="Send a direct message withiut starting the client.",
    )

    args = parser.parse_args()

    channel = args.channel
    if not channel:
        channel = "global"

    TOPIC = f"{TOPIC}/{channel}"

    if args.direct:
        send_message(args.direct)
        exit(0)

    print(f"Welcome to CryptaQueue Chat Sender.")
    print(f"Broker address: {BROKER_ADDRESS}")
    print(f"Chat Username: {CHAT_USERNAME}")
    print(f"Topic: {TOPIC}")

    while True:
        try:
            print(">", end=" ")
            msg = input()
            if msg == "exit":
                break
        except KeyboardInterrupt:
            exit()

        if msg:
            send_message(msg)
