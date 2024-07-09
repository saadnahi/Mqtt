import paho.mqtt.client as mqtt
import logging

logger = logging.getLogger(__name__)

class ServerManager:
    def __init__(self, config):
        self.client_id = config['client_id']
        self.address = config['address']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.config = config
        self.client = mqtt.Client(client_id=config['client_id'])
        self.client.username_pw_set(config['username'], config['password'])
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.topics = {}
        self.decoders = {}

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
            self.topics[topic] = None
        except Exception as e:
            logger.error(f"Failed to subscribe to topic {topic}: {e}")

    def unsubscribe(self, topic):
        try:
            self.client.unsubscribe(topic)
            if topic in self.topics:
                del self.topics[topic]
        except Exception as e:
            logger.error(f"Failed to unsubscribe from topic {topic}: {e}")

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected to {client._host} with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logger.info(f"Disconnected from {client._host}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload
        if topic in self.decoders:
            try:
                self.decoders[topic](payload)
            except Exception as e:
                logger.error(f"Failed to decode message on topic {topic}: {e}")
        else:
            logger.warning(f"No decoder for topic: {topic}")

   