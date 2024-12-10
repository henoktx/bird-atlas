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
    def get(
            self,
            scientific_name: Optional[str],
            common_name: Optional[str],
            location: Optional[str],
            average_size: Optional[float],
            average_weight: Optional[float],
            life_expectancy: Optional[int]
    ) -> list[Bird]:
        pass

    @abstractmethod
    def _generate_next_id(self) -> int:
        pass