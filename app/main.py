import sys
import os

from shared.config import Config
from files.infrastructure.mongo_file_repository import MongoFileRepository
from files.application.file_commands import GetFileCommand, SaveFileCommand
from messages.infrastructure.rabbitmq_messages_service import (
    RabbitMQMessagingService,
)


def main():
    config = Config()
    file_repository = MongoFileRepository(config.db_uri, config.db_name)
    messages_service = RabbitMQMessagingService(
        host=config.rabbitmq_host,
        user=config.rabbitmq_user,
        password=config.rabbitmq_password,
        port=config.rabbitmq_port,
        source=config.source,
    )

    def process_message(message, properties):
        try:
            asset_id = message.get("asset_id")
            file = GetFileCommand(file_repository).execute(asset_id)

            if not file:
                raise Exception(f"File with id: '{asset_id}' was not found")

            new_asset_id = SaveFileCommand(file_repository).execute(
                filename=file.filename, content=file.content
            )

            messages_service.publish(
                {
                    "asset_id": new_asset_id,
                    "options": getattr(message, "options", {}),
                    "status": "normal",
                },
                config.queue_name_send,
                properties.correlation_id,
            )
            print(f"New file '{new_asset_id}' was uploaded")
        except Exception as e:
            print(e)
            messages_service.publish(
                {
                    "asset_id": message.get("asset_id"),
                    "options": getattr(message, "options", {}),
                    "status": "error",
                    "error": str(e),
                },
                config.queue_name_send,
                properties.correlation_id,
            )

    print("Waiting for messages...")
    messages_service.subscribe(queue=config.queue_name, callback=process_message)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
