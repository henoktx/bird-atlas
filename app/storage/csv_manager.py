import csv
from os import path
from typing import Optional

from app.model.Bird import Bird
from app.storage.storage_manager import IStorageManager
from app.util.csv_serializer import CSVSerializer
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

    def count_birds(self) -> int:
        self.file.seek(0, 0)

        return len(self.file.readlines()) - 1

    def save(self, bird: Bird) -> Bird:
        csv.writer(self.file).writerow(self.serializer.serializer(bird))
        self.file.flush()

        return bird

    def update(self, old_scientific_name: str, bird: Bird) -> Bird:
        try:
            self.delete(old_scientific_name)
        except ValueError as error:
            raise ValueError(f"Cannot update - {error}")

        return self.save(bird)

    def delete(self, scientific_name: str) -> None:
        if not self.scientific_name_exists(scientific_name):
            raise ValueError(f"Bird with ID {scientific_name} not found")

        self.file.seek(0, 0)

        csv_reader = csv.reader(self.file)
        next(csv_reader)

        new_bird_list = [line for line in csv_reader
                         if self.serializer.deserializer(line).scientific_name != scientific_name]

        self.file.seek(0, 0)
        self.file.truncate()

        csv_writer = csv.writer(self.file)

        csv_writer.writerow(CSV_HEADERS)
        csv_writer.writerows(new_bird_list)

        self.file.flush()

    def scientific_name_exists(self, scientific_name: str) -> bool:
        self.file.seek(0, 0)

        csv_reader = csv.reader(self.file)
        next(csv_reader)

        for line in csv_reader:
            actual_bird = self.serializer.deserializer(line)
            if actual_bird.scientific_name == scientific_name:
                return True

        return False
