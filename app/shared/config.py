import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv(dotenv_path=".env", override=True)


class Config:
    # Gral
    source = os.getenv(key="SOURCE", default="aa-microservice.template-python")

    # RabbitMQ
    rabbitmq_host = os.getenv(key="RABBITMQ_HOST", default="rabbitmq")
    rabbitmq_port = os.getenv(key="RABBITMQ_PORT", default="5672")
    rabbitmq_user = os.getenv(key="RABBITMQ_USER", default="guest")
    rabbitmq_password = os.getenv(key="RABBITMQ_PASSWORD", default="guest")
    exchange = os.getenv(key="RABBITMQ_EXCHANGE", default="assets")
    queue_name = os.getenv(key="RABBITMQ_QUEUE_RECEIVE", default="assets.template.1")
    binding_key = os.getenv(key="RABBITMQ_BINDING_KEY", default="assets.template.1")
    queue_name_send = os.getenv(key="RABBITMQ_QUEUE_SEND", default="assets.processed.1")

    # MongoDB
    db_uri = os.getenv(key="MONGO_URI", default="mongodb://localhost:27017/")
    db_name = os.getenv(key="MONGO_DB_NAME", default="storage")
