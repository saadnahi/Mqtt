from models import Session, Server, Topic, Decoder
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.session = Session()

    def add_server(self, server_config):
        try:
            # Check if the server with the given address already exists
            existing_server = self.session.query(Server).filter_by(address=server_config['address']).first()
            
            if existing_server:
                # Log a message if the server already exists and return its ID
                logger.info(f"Server with address {server_config['address']} already exists.")
                return existing_server.id
            
            # If the server does not exist, create a new server object and add it to the session
            new_server = Server(
                address=server_config['address'],
                port=server_config['port'],
                username=server_config['username'],
                password=server_config['password'],
                project_id=server_config['project_id']
            )
            self.session.add(new_server)
            self.session.commit()  # Commit the session to save the new server to the database
            logger.info("Server added successfully")
            return new_server.id
        except Exception as e:
            self.session.rollback()  # Rollback the session in case of an error
            raise RuntimeError(f"Failed to add server to the database: {e}")

    def remove_server(self, server_id):
        # Query the database for the server with the given ID
        server = self.session.query(Server).filter_by(id=server_id).first()
        if server:
            # Delete the server if it exists
            self.session.delete(server)
            self.session.commit()  # Commit the session to save the changes
            logger.info("Server removed successfully")
        else:
            raise ValueError(f"No server found with ID: {server_id}")

    def get_server(self, server_id):
        # Query the database for the server with the given ID and return it
        return self.session.query(Server).filter_by(id=server_id).first()

    def add_topic(self, server_id, topic_name):
        try:
            # Check if the topic already exists for the given server
            existing_topic = self.session.query(Topic).filter_by(server_id=server_id, topic_name=topic_name).first()
            
            if existing_topic:
                # Log a warning if the topic already exists and return its ID
                logger.warning(f"Topic '{topic_name}' already exists for server ID {server_id}.")
                return existing_topic.id
            
            # If the topic does not exist, create a new topic object and add it to the session
            new_topic = Topic(server_id=server_id, topic_name=topic_name)
            self.session.add(new_topic)
            self.session.commit()  # Commit the session to save the new topic to the database
            logger.info("Topic added successfully")
            return new_topic.id
        except Exception as e:
            self.session.rollback()  # Rollback the session in case of an error
            raise RuntimeError(f"Failed to add topic '{topic_name}' for server ID {server_id}: {e}")
        
    def remove_topic(self, topic_id):
        # Query the database for the topic with the given ID
        topic = self.session.query(Topic).filter_by(id=topic_id).first()
        if topic:
            # Delete the topic if it exists
            self.session.delete(topic)
            self.session.commit()  # Commit the session to save the changes
            logger.info("Topic removed successfully")
        else:
            raise ValueError(f"No topic found with ID: {topic_id}")

    def get_topics(self, server_id):
        # Query the database for all topics associated with the given server ID and return them
        return self.session.query(Topic).filter_by(server_id=server_id).all()
    
    def get_topic_id_by_name(self, topic_name):
        try:
            # Query the database for the topic with the given topic_name
            topic = self.session.query(Topic).filter_by(topic_name=topic_name).first()
            
            if topic:
                # Return the topic_id if the topic is found
                return topic.id
            else:
                # Log a warning if the topic is not found
                logger.warning(f"No topic found with name '{topic_name}'.")
                return None
        except Exception as e:
            # Handle exceptions 
            raise RuntimeError(f"Failed to retrieve topic ID for topic name '{topic_name}': {e}")

    def add_decoder(self, topic_name, decoder_function):
        try:
            topic_id = self.get_topic_id_by_name(topic_name)
            if topic_id is None:
                raise ValueError(f"No topic found for name '{topic_name}'")

            existing_decoder = self.session.query(Decoder).filter_by(topic_id=topic_id).first()
            if existing_decoder:
                logger.warning(f"Decoder for topic ID {topic_id} already exists.")
                return existing_decoder.id

            new_decoder = Decoder(topic_id=topic_id, decoder_function=decoder_function)
            self.session.add(new_decoder)
            self.session.commit()
            logger.info("Decoder added successfully to the database")
            return new_decoder.id
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Failed to add decoder function to the database: {e}")

    def remove_decoder(self, decoder_id):
        # Query the database for the decoder with the given ID
        decoder = self.session.query(Decoder).filter_by(id=decoder_id).first()
        if decoder:
            # Delete the decoder if it exists
            self.session.delete(decoder)
            self.session.commit()  # Commit the session to save the changes
            logger.info("Decoder removed successfully")
        else:
            raise ValueError(f"No decoder function found with ID: {decoder_id}")
    
    def get_decoder_by_topic(self, topic_name):
        try:
            topic = self.session.query(Topic).filter_by(topic_name=topic_name).first()
            if topic:
                decoder = self.session.query(Decoder).filter_by(topic_id=topic.id).first()
                if decoder:
                    return decoder.decoder_function
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve decoder for topic '{topic_name}': {e}")