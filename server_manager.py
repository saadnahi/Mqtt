import paho.mqtt.client as mqtt
from models import Session, Topic, Decoder
import logging

class ServerManager:
    def __init__(self, config):
        self.client_id = config['client_id']
        self.config = config
        self.client = mqtt.Client(client_id=config['client_id'])
        self.client.username_pw_set(config['username'], config['password'])
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.topics = {}
        self.decoders = {}

    def connect(self):
        self.client.connect(self.config['address'], self.config['port'])
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.topics[topic] = None
        # Add topic to the database
        session = Session()
        db_topic = Topic(server_id=self.client_id, topic_name=topic)
        session.add(db_topic)
        session.commit()

    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)
        if topic in self.topics:
            del self.topics[topic]
        # Remove topic from the database
        session = Session()
        db_topic = session.query(Topic).filter_by(topic_name=topic).first()
        if db_topic:
            session.delete(db_topic)
            session.commit()

    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"Connected to {self.config['address']} with result code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logging.info(f"Disconnected from {self.config['address']}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload
        if topic in self.decoders:
            self.decoders[topic](payload)
        else:
            logging.warning(f"No decoder for topic: {topic}")

    def add_decoder(self, topic, decoder_function):
        self.decoders[topic] = decoder_function
        # Add decoder to the database
        session = Session()
        db_topic = session.query(Topic).filter_by(topic_name=topic).first()
        if db_topic:
            db_decoder = Decoder(topic_id=db_topic.id, decoder_function=decoder_function)
            session.add(db_decoder)
            session.commit()