# CryptaQueue
Send Encrypted message to your group, via MQTT.

## Quick Start
This quick start is created for Debian-based systems.

1. Run the installation script:
    ```bash
    ./install.sh
    ```
2. Create a .env file, starting from the template (.env.template):
    ```bash
    cp .env.template .env
    nano .env
    ```
    You can generate a random base64 IV string running this command in a shell:
    ```bash
    openssl rand -base64 16
    ```
3. Run the unified client:
    ```bash
    ./cq.sh
    ```