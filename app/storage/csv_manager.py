from typing import Optional

from app.model.Bird import Bird
from app.storage.storage_manager import IStorageManager


class CSVManager(IStorageManager):
    def save(self, bird: Bird) -> Bird:
        pass

    def update(self, bird: Bird) -> Bird:
        pass

    def delete(self, bird_id: int) -> None:
        pass

    def get(self, search: Optional[str] = None) -> list[Bird]:
        pass