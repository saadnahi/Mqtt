# I should modify the entire main don't pay attention to it 

from mqtt_client_manager import MQTTClientManager
from server_manager import ServerManager
from topic_manager import TopicManager
from decoder_manager import DecoderManager
import logging

# Configure logging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Create instances of the manager classes.
        client_manager = MQTTClientManager()
        topic_manager = TopicManager(server_manager)

        # Example server configuration.
        server_config = {
            'address': 'eu1.cloud.thethings.network',
            'port': 1883,
            'username': 'soil-devices@ttn',
            'password': 'NNSXS.GHIOPEDQOOUFUFK5W2NLKYVIRJSUJR57DDCYUUQ.XLPL6YUEDFX7LH6KJX2DZLVJSE6S7EG62FFWKL4VSIRUBQ7W464A',
            'client_id': 'soil-devices'
        }

        # Add the server configuration to the client manager.
        client_manager.add_server(server_config)
        logger.info("Server added successfully")

        # Get the server configuration from the client manager.
        server = client_manager.get_server('soil-devices')  # Ensure this ID matches the one in the database
        if server:
            # Correctly instantiate the ServerManager with the server configuration.
            server_config = {
                'address': server.address,
                'port': server.port,
                'username': server.username,
                'password': server.password,
                'client_id': server.client_id
            }
            server_manager = ServerManager(server_config)
            server_manager.connect()
            logger.info("Connected to the server")

            # Initialize DecoderManager with the ServerManager instance
            decoder_manager = DecoderManager(server_manager)

            # Example topic and decoder addition.
            topic_manager.add_topic(1, 'example/topic')
            logger.info("Topic added successfully")
            
            def decode(payload):
                return payload.decode('utf-8')
            
            decoder_manager.add_decoder('example/topic', decode)
            logger.info("Decoder added successfully")

            # Subscribe to the topics associated with the server.
            topics = topic_manager.get_topics(1)
            for topic in topics:
                server_manager.subscribe(topic)
                logger.info(f"Subscribed to topic: {topic}")

            # Example payload decoding.
            payload = b'example payload'
            decoded_payload = decoder_manager.decode('example/topic', payload)
            logger.info(f"Decoded payload: {decoded_payload}")
        else:
            logger.error("Server not found.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()