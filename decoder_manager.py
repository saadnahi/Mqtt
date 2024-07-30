from database_manager import DatabaseManager
import logging
import json 

logger = logging.getLogger(__name__)

class DecoderManager:
    def __init__(self):
        self.decoders = {}  # Dictionary to store topics and associated decoder functions
        self.db_manager = DatabaseManager()

    def add_decoder(self, topic, decoder_function):
        try:
            self.decoders[topic] = decoder_function
            logger.info(f"Added decoder function for topic {topic} to the dic")

            self.db_manager.add_decoder(topic, decoder_function)
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
            # Check if the decoder function code is already in the local dictionary
            if topic in self.decoders:
                decoder_function_code = self.decoders[topic]
            else:
                # Retrieve the decoder function code from the database
                decoder_function_code = self.db_manager.get_decoder_by_topic(topic)
                if decoder_function_code:
                    # Store the retrieved decoder function code in the local dictionary
                    self.decoders[topic] = decoder_function_code
                else:
                    # Log a warning and return None if no decoder function is found
                    logger.warning(f"No decoder function found for topic {topic}")
                    return None

            # Prepare the local execution environment with the json module
            local_vars = {}

            # Execute the decoder function code
            exec(decoder_function_code, globals(), local_vars)

            # Retrieve the decode_payload function from the local_vars dictionary
            decoder_function = local_vars.get('decode_payload')

            if decoder_function:
                 # Decode the byte payload to a string
                #payload_str = payload.decode('utf-8')
                #logger.info(f"Received message on topic {topic}: {payload_str}")
                # Parse the payload from JSON to a Python dictionary
                #payload_dict = json.loads(payload_str)
                
                # Log the decoding action and call the decoder function with the parsed payload
                logger.info(f"Decoding message on topic {topic} using retrieved decoder function...")
                return decoder_function(payload)
            else:
                # Log an error if the decode_payload function is not found
                logger.error(f"Failed to retrieve 'decode_payload' function from the code for topic {topic}")
                return None

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e} - Payload: {payload}")
            return None
        except Exception as e:
            # Log any other exceptions that occur during the decoding process
            logger.error(f"Failed to decode message on topic {topic}: {e}")
            return None