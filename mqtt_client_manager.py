import paho.mqtt.client as mqtt
from models import Session, Server

class MQTTClientManager:
    def __init__(self):
        self.servers = []

    def add_server(self, server_config):
        server = mqtt.Client(client_id=server_config['client_id'])
        server.username_pw_set(server_config['username'], server_config['password'])
        server.connect(server_config['address'], server_config['port'])
        self.servers.append(server)

        # Add server to the database
        session = Session()
        new_server = Server(
            address=server_config['address'],
            port=server_config['port'],
            username=server_config['username'],
            password=server_config['password'],
            client_id=server_config['client_id']
        )
        session.add(new_server)
        session.commit()

    def remove_server(self, server_id):
        # Remove server from the list and the database
        session = Session()
        server = session.query(Server).filter_by(id=server_id).first()
        if server:
            self.servers = [s for s in self.servers if s._client_id != server.client_id]
            session.delete(server)
            session.commit()

    def get_server(self, server_id):
        session = Session()
        return session.query(Server).filter_by(id=server_id).first()
