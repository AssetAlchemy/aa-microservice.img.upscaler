from abc import ABC, abstractmethod
from typing import Callable

from messages.domain.message import Message


class MessagesService(ABC):
    @abstractmethod
    def publish(self, message: Message, topic: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[dict], None]) -> None:
        raise NotImplementedError
