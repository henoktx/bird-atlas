import csv
from os import path
from typing import Optional

from app.model.Bird import Bird
from app.storage.storage_manager import IStorageManager
from app.storage.csv.csv_serializer import CSVSerializer


CSV_HEADERS = list(Bird.__annotations__.keys())

class CSVManager(IStorageManager):
    def __init__(self, file_path: str, serializer: CSVSerializer):
        has_file = path.exists(file_path)

        self.file_path = file_path
        self.file = open(self.file_path, "a+")
        self.serializer = serializer

        if not has_file:
            csv.writer(self.file).writerow(CSV_HEADERS)
            self.file.flush()

    def save(self, bird: Bird) -> Bird:
        bird.id = self._generate_next_id()

        csv.writer(self.file).writerow(self.serializer.serializer(bird))
        self.file.flush()

        return bird

    def update(self, bird: Bird) -> Bird:
        pass

    def delete(self, bird_id: int) -> None:
        pass

    def get(self, search: Optional[str] = None) -> list[Bird]:
        pass

    def _generate_next_id(self) -> int:
        with open(self.file_path, "r") as db:
            lines = sum(1 for _ in db)
            return lines