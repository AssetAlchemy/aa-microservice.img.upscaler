import pika
import json
import uuid

from typing import Callable

import pika.spec
from messages.domain.messages_service import MessagesService


class RabbitMQMessagingService(MessagesService):
    def __init__(self, host: str, user: str, password: str, port: str, source: str):
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.port: str = port
        self.source: str = source
        self.connection = None
        self.channel = None

    def _connect(self):
        if not self.connection or self.channel:
            self.credentials = pika.PlainCredentials(self.user, self.password)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host, port=self.port, credentials=self.credentials
                )
            )
            self.channel = self.connection.channel()

    def _validate_properties(self, message_id, correlation_id, app_id, content_type):
        if message_id is None:
            raise Exception("No 'message_id' on properties")
        if correlation_id is None:
            raise Exception("No 'correlation_id' on properties")
        if app_id is None:
            raise Exception("No 'app_id' on properties")
        if content_type is None:
            raise Exception("No 'content_type' on properties")
        if content_type != "application/json":
            raise Exception("'content_type' on properties should be 'application/json'")

    def publish(self, message: dict, queue: str, correlation_id: str) -> None:
        self._connect()

        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                app_id=self.source,
                content_type="application/json",
                message_id=str(uuid.uuid4()),
                correlation_id=correlation_id,
            ),
        )

    def subscribe(
        self, queue: str, callback: Callable[[dict, pika.BasicProperties], None]
    ) -> None:
        self._connect()

        self.channel.queue_declare(queue=queue, durable=True)

        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body.decode("utf-8"))
                asset_id = message.get("asset_id")

                self._validate_properties(
                    message_id=properties.message_id,
                    correlation_id=properties.correlation_id,
                    app_id=properties.app_id,
                    content_type=properties.content_type,
                )
                if asset_id is None:
                    raise Exception("No 'asset_id' on message body")

                callback(message, properties)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except json.JSONDecodeError:
                print("Error to parse message")
                self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                print(e)
                self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        self.channel.basic_consume(queue=queue, on_message_callback=on_message)
        print(f"Listening on {queue}...")
        self.channel.start_consuming()
