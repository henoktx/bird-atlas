import csv
from os import path
from typing import Optional

from app.model.Bird import Bird
from app.storage.storage_manager import IStorageManager
from app.storage.csv.csv_serializer import CSVSerializer
from app.util.match_attribute import Matcher

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

    def get(
        self,
        scientific_name: Optional[str],
        common_name: Optional[str],
        location: Optional[str],
        average_size: Optional[float],
        average_weight: Optional[float],
        life_expectancy: Optional[int]
    ) -> list[Bird]:
        self.file.seek(0, 0)

        csv_reader = csv.reader(self.file)
        next(csv_reader)

        birds = [
            bird for line in csv_reader
            if (
                (bird := self.serializer.deserializer(line))
                and Matcher.match_str_attribute(scientific_name, bird.scientific_name)
                and Matcher.match_str_attribute(common_name, bird.common_name)
                and Matcher.match_str_attribute(location, bird.location)
                and Matcher.match_numeric_attribute(average_size, bird.average_size)
                and Matcher.match_numeric_attribute(average_weight, bird.average_weight)
                and Matcher.match_numeric_attribute(life_expectancy, bird.life_expectancy)
            )
        ]

        return birds

    def _generate_next_id(self) -> int:
        with open(self.file_path, "r") as db:
            lines = sum(1 for _ in db)
            return lines