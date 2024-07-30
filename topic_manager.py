from database_manager import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class TopicManager:
    def __init__(self):
        self.topics = {}  # Dictionary to store topics and associated servers
        self.db_manager = DatabaseManager()

    def add_topic(self, server_id, topic):
        try:
            # Add topic subscription to the database
            self.db_manager.add_topic(server_id, topic)
            self.topics[topic] = server_id  # Update local topics dictionary
            logger.info(f"Topic added successfully to the dic")
        except Exception as e:
            logger.error(f"Failed to add topic {topic} for server ID {server_id}: {e}")

    def remove_topic(self, topic):
        try:
            # Remove topic subscription from the database
            topic_id = self.db_manager.get_topic_id_by_name(topic)
            if topic_id:
                self.db_manager.remove_topic(topic_id)
                if topic in self.topics:
                    del self.topics[topic]     # Remove from local topics dictionary
                logger.info(f"Removed topic {topic} from the database")
            else:
                logger.warning(f"Topic {topic} not found")
        except Exception as e:
            logger.error(f"Failed to remove topic {topic}: {e}")

    def get_topics(self, server_id):
        try:
            # Retrieve topics for a specific server from the database
            topics = self.db_manager.get_topics(server_id)
            topic_names = [topic.topic_name for topic in topics]
            for topic in topic_names:
                self.topics[topic] = server_id  # Update local topics dictionary
            logger.info(f"Retrieved topics for server ID {server_id} from the database: {topic_names}")
            return topic_names
        except Exception as e:
            logger.error(f"Failed to get topics for server ID {server_id}: {e}")
            return []