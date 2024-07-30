from database_manager import DatabaseManager
from server_manager import ServerManager
import logging

logger = logging.getLogger(__name__)

class MQTTClientManager:
    def __init__(self):
        self.servers = {}
        self.db_manager = DatabaseManager()

    def add_server(self, server_config):
        address = server_config['address']
        if address not in self.servers:
            try:
                server_id = self.db_manager.add_server(server_config)
                server = ServerManager(server_config)
                server.connect()
                self.servers[address] = server
                logger.info(f"Connected to server at {address}, Server ID: {server_id}")
            except Exception as e:
                logger.error(f"Failed to connect to server at {address}: {e}")
        else:
            logger.warning(f"Server with address {address} already exists.")

    def remove_server(self, server_id):
        try:
            server = self.db_manager.get_server(server_id)
            if server:
                address = server.address
                mqtt_server = ServerManager(address)
                mqtt_server.disconnect()
                logger.info(f"Disconnected and removed server at {address}")
                self.db_manager.remove_server(server_id)
            else:
                logger.error(f"No server found with ID: {server_id}")
        except Exception as e:
            logger.error(f"Error removing server: {e}")

    def get_server(self, server_id):
        try:
            server = self.db_manager.get_server(server_id)
            if server:
                return server
            else:
                logger.error(f"No server found with ID: {server_id}")
        except Exception as e:
            logger.error(f"Error retrieving server: {e}")
            return None