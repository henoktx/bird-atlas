from abc import ABC, abstractmethod
from typing import Optional

from app.model.Bird import Bird


class IStorageManager(ABC):
    @abstractmethod
    def save(self, bird: Bird) -> Bird:
        pass

    @abstractmethod
    def update(self, bird: Bird) -> Bird:
        pass

    @abstractmethod
    def delete(self, bird_id: int) -> None:
        pass

    @abstractmethod
    def get(self, search: Optional[str] = None) -> list[Bird]:
        pass