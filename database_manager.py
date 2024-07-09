from models import Session, Server, Topic, Decoder

class DatabaseManager:
    def __init__(self):
        self.session = Session()

    def add_server(self, server_config):
        try:
            new_server = Server(
                address=server_config['address'],
                port=server_config['port'],
                username=server_config['username'],
                password=server_config['password'],
                client_id=server_config['client_id']
            )
            self.session.add(new_server)
            self.session.commit()
            return new_server.id
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Failed to add server to the database: {e}")

    def remove_server(self, server_id):
        server = self.session.query(Server).filter_by(id=server_id).first()
        if server:
            self.session.delete(server)
            self.session.commit()
        else:
            raise ValueError(f"No server found with ID: {server_id}")

    def get_server(self, server_id):
        return self.session.query(Server).filter_by(id=server_id).first()

    def add_topic(self, server_id, topic_name):
        try:
            new_topic = Topic(server_id=server_id, topic_name=topic_name)
            self.session.add(new_topic)
            self.session.commit()
            return new_topic.id
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Failed to add topic to the database: {e}")

    def remove_topic(self, topic_id):
        topic = self.session.query(Topic).filter_by(id=topic_id).first()
        if topic:
            self.session.delete(topic)
            self.session.commit()
        else:
            raise ValueError(f"No topic found with ID: {topic_id}")

    def get_topics(self, server_id):
        return self.session.query(Topic).filter_by(server_id=server_id).all()

    def add_decoder(self, topic_id, decoder_function):
        try:
            new_decoder = Decoder(topic_id=topic_id, decoder_function=decoder_function)
            self.session.add(new_decoder)
            self.session.commit()
            return new_decoder.id
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Failed to add decoder function to the database: {e}")

    def remove_decoder(self, decoder_id):
        decoder = self.session.query(Decoder).filter_by(id=decoder_id).first()
        if decoder:
            self.session.delete(decoder)
            self.session.commit()
        else:
            raise ValueError(f"No decoder function found with ID: {decoder_id}")