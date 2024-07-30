import paho.mqtt.client as mqtt
from decoder_manager import DecoderManager
import logging
import json
from tabulate import tabulate

logger = logging.getLogger(__name__)

class ServerManager:
    def __init__(self, config):
        self.project_id = config['project_id']
        self.address = config['address']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.config = config

        self.client = mqtt.Client()
        self.client.username_pw_set(config['username'], config['password'])
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.decoder_manager = DecoderManager()

        self.message_count = 0  # Counter for received messages
    

    def connect(self):
        try:
            self.client.connect(self.address, self.port)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Failed to connect to MQTT server: {e}")
            raise

    def disconnect(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            logger.error(f"Failed to disconnect from MQTT server: {e}")

    def subscribe(self, topic):
        try:
            self.client.subscribe(topic)
            logger.info(f'subscribed to topic {topic}')
        except Exception as e:
            logger.error(f"Failed to subscribe to topic {topic}: {e}")

    def unsubscribe(self, topic):
        try:
            self.client.unsubscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")
        except Exception as e:
            logger.error(f"Failed to unsubscribe from topic {topic}: {e}")

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to MQTT server")

    def on_disconnect(self, client, userdata, rc):
        logger.info("Disconnected from MQTT server")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8') 

        try:
            #logger.info(f"Received message on topic {topic}: {payload}")
            logger.info(f"Payload type: {type(payload)}")
            # Decode the message
            decoded_data = self.decoder_manager.decode(topic, payload)
            # Process the decoded data
            if decoded_data:
                # Display decoded data in table format
                table = tabulate(decoded_data.items(), headers=["Field", "Value"], tablefmt="presto")
                logger.info(f"Decoded data for topic {topic}:\n{table}")
            # Increment the message count
            self.message_count += 1
            if self.message_count >= 5:
                logger.info("Received 5 messages. Disconnecting...")
                self.disconnect()
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e} - Payload: {payload}")
        except Exception as e:
            logger.error(f"Failed to decode message on topic {topic}: {e}")

   