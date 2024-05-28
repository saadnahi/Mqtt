class TopicManager:
    def __init__(self):
        self.topics = {}

    def add_topic(self, server_id, topic):
        self.topics[topic] = server_id

    def remove_topic(self, topic):
        if topic in self.topics:
            del self.topics[topic]

    def get_topics(self, server_id):
        return [t for t, s_id in self.topics.items() if s_id == server_id]