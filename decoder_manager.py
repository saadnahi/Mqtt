from database_manager import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class DecoderManager:
    def __init__(self):
        self.decoders = {}  # Dictionary to store topics and associated decoder functions
        self.db_manager = DatabaseManager()

    def add_decoder(self, topic, decoder_function):
        try:
            # Add decoder function to local dictionary
            self.decoders[topic] = decoder_function
            logger.info(f"Added decoder function for topic {topic}")

            # Add decoder function to the database
            topic_id = self.db_manager.add_decoder(topic, decoder_function.__name__)
            logger.info(f"Added decoder function for topic {topic} to the database, Decoder ID: {topic_id}")
        except Exception as e:
            logger.error(f"Failed to add decoder function for topic {topic}: {e}")

    def remove_decoder(self, topic):
        try:
            # Remove decoder function from local dictionary
            if topic in self.decoders:
                del self.decoders[topic]
                logger.info(f"Removed decoder function for topic {topic}")

            # Remove decoder function from the database
            decoders = self.db_manager.get_decoders()
            decoder_id = None
            for d in decoders:
                if d.topic == topic:
                    decoder_id = d.id
                    break
            if decoder_id:
                self.db_manager.remove_decoder(decoder_id)
                logger.info(f"Removed decoder function for topic {topic} from the database, Decoder ID: {decoder_id}")
            else:
                logger.warning(f"Decoder function for topic {topic} not found in the database")
        except Exception as e:
            logger.error(f"Failed to remove decoder function for topic {topic}: {e}")

    def decode(self, topic, payload):
        try:
            # Retrieve decoder function from local dictionary
            if topic in self.decoders:
                decoder_function = self.decoders[topic]
                logger.info(f"Decoding message on topic {topic} using decoder function {decoder_function.__name__}")
                return decoder_function(payload)
            else:
                logger.warning(f"No decoder function found for topic {topic}")
                return None
        except Exception as e:
            logger.error(f"Failed to decode message on topic {topic}: {e}")
            return None