from mqtt_client_manager import MQTTClientManager
from server_manager import ServerManager
from topic_manager import TopicManager
from decoder_manager import DecoderManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        client_manager = MQTTClientManager()
        topic_manager = TopicManager()
        decoder_manager = DecoderManager()

        # Example server configuration
        server_config = {
            'address': 'mqtt.example.com',
            'port': 1883,
            'username': 'user',
            'password': 'pass',
            'client_id': 'client1'
        }

        client_manager.add_server(server_config)
        logger.info("Server added successfully")

        # Example topic and decoder addition
        topic_manager.add_topic(1, 'example/topic')
        decoder_function = '''
        def decode(payload):
            return payload.decode('utf-8')
        '''
        decoder_manager.add_decoder('example/topic', decoder_function)
        logger.info("Topic and decoder added successfully")

        # Connect to the server and subscribe to topics
        server = client_manager.get_server(1)
        server_manager = ServerManager(
            server.address, server.port, server.username, server.password, server.client_id
        )
        server_manager.connect()
        logger.info("Connected to the server")

        topics = topic_manager.get_topics(1)
        for topic in topics:
            server_manager.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")

        # Example payload decoding
        payload = b'example payload'
        decoded_payload = decoder_manager.decode('example/topic', payload)
        logger.info(f"Decoded payload: {decoded_payload}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()