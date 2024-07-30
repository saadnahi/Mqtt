from mqtt_client_manager import MQTTClientManager
from server_manager import ServerManager
from topic_manager import TopicManager
from decoder_manager import DecoderManager
import time
import logging

decoder_func = '''def decode_payload(payload):
    import json
    try:
        # Convert JSON string to dictionary
        payload_dict = json.loads(payload)

        # Process the payload dictionary
        device_id = payload_dict["end_device_ids"]["device_id"]
        received_at = payload_dict["received_at"]
        uplink_message = payload_dict["uplink_message"]
        decoded_payload = uplink_message["decoded_payload"]
        
        # Extract necessary fields from the decoded_payload
        battery = decoded_payload["Bat"]
        interrupt_flag = decoded_payload["Interrupt_flag"]
        leaf_moisture = decoded_payload["Leaf_Moisture"]
        leaf_temperature = decoded_payload["Leaf_Temperature"]
        
        # Return the extracted data or any other required processing
        return {
            "device_id": device_id,
            "received_at": received_at,
            "battery": battery,
            "interrupt_flag": interrupt_flag,
            "leaf_moisture": leaf_moisture,
            "leaf_temperature": leaf_temperature
        }
    except Exception as e:
        logger.error(f"Error in decode_payload: {e}")
        return None'''
                
# Configure logging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Create instances of the manager classes.
        client_manager = MQTTClientManager()
        topic_manager = TopicManager()
        decoder_manager = DecoderManager()

        # Example server configuration.
        server_config = {
            'address': 'eu1.cloud.thethings.network',
            'port': 1883,
            'username': 'soil-devices@ttn',
            'password': 'NNSXS.3VXRVN56FRYZX75WFGW3WLRPRAURNQN6HL6GGSI.NW2XJVTXYLVD3HEYN2P4E2WIHXJYWD7TZJYZA45QMHK5BXXDO5SA',
            'project_id': 'soil-devices' #project id
        }

        # Add the server configuration to the client manager.
        client_manager.add_server(server_config)
        
        # Get the server configuration from the client manager.
        server = client_manager.get_server(1)  # Ensure this ID matches the one in the database
        if server:
            # Correctly instantiate the ServerManager with the server configuration.
            server_config = {
                'address': server.address,
                'port': server.port,
                'username': server.username,
                'password': server.password,
                'project_id': server.project_id
            }
            server_manager = ServerManager(server_config)
            server_manager.connect()

            topic = 'v3/soil-devices@ttn/devices/eui-a84041d3b187e578/up'
            # Topic and decoder addition.
            topic_manager.add_topic(1, topic)
            decoder_manager.add_decoder(topic,decoder_func)

            # Subscribe to the topics associated with the server.
            topics = topic_manager.get_topics(1)
            for topic in topics:
                server_manager.subscribe(topic)
            # Keep the main thread alive
            logger.info("Listening for messages... ")
            try:
                 while True:
                    time.sleep(10)  # Sleep to keep the script running
                    #pass
            except KeyboardInterrupt:
                server_manager.disconnect()

        else:
            logger.error("Server not found.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()