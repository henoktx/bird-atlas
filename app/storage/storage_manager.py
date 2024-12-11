from abc import ABC, abstractmethod
from typing import Optional
from zipfile import ZipFile

from app.model.Bird import Bird


class IStorageManager(ABC):
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
    def count_birds(self) -> int:
        pass

    @abstractmethod
    def save(self, bird: Bird) -> Bird:
        pass

    @abstractmethod
    def update(self, old_scientific_name: str, bird: Bird) -> Bird:
        pass

    @abstractmethod
    def delete(self, scientific_name: str) -> None:
        pass

    @abstractmethod
    def scientific_name_exists(self, scientific_name: str) -> bool:
        pass