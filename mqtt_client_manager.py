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
                # Instantiate ServerManager and store it
                self.servers[address] = ServerManager(server_config)
                logger.info(f"Server with address {address} and ID: {server_id} added")
            except Exception as e:
                logger.error(f"Failed to add the server at {address}: {e}")
        else:
            logger.warning(f"Server with address {address} already exists.")

    def remove_server(self, server_id):
        try:
            server = self.db_manager.get_server(server_id)
            if server:
                address = server.address
                # Ensure the server is removed from both DB and the in-memory dictionary
                if address in self.servers:
                    del self.servers[address]
                self.db_manager.remove_server(server_id)
                logger.info(f"Removed server at {address}")
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
                return None  
        except Exception as e:
            logger.error(f"Error retrieving server: {e}")
            return None  