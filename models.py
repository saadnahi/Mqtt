from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Update to use sqlalchemy.orm.declarative_base
Base = declarative_base()

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    address = Column(String)
    port = Column(Integer)
    username = Column(String)
    password = Column(String)
    project_id = Column(String)

class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    topic_name = Column(String)
    server = relationship("Server", back_populates="topics")

class Decoder(Base):
    __tablename__ = 'decoders'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    decoder_function = Column(String)
    topic = relationship("Topic", back_populates="decoders")

Server.topics = relationship("Topic", order_by=Topic.id, back_populates="server")
Topic.decoders = relationship("Decoder", order_by=Decoder.id, back_populates="topic")

engine = create_engine('sqlite:///mqtt_client.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)