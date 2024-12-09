import csv
from io import StringIO
from typing import Dict

from app.model.Bird import Bird


class CSVSerializer:
    @staticmethod
    def serializer(bird: Bird) -> list[any]:
        return [bird.id,
                bird.scientific_name,
                bird.common_name,
                bird.location,
                bird.average_size,
                bird.average_weight,
                bird.life_expectancy,
                bird.photo]

    @staticmethod
    def deserializer(self, serialized_bird: list[any]) -> Bird:
        return Bird(
            id=serialized_bird[0],
            scientific_name=serialized_bird[1],
            common_name=serialized_bird[2],
            location=serialized_bird[3],
            average_size=serialized_bird[4],
            average_weight=serialized_bird[5],
            life_expectancy=serialized_bird[6],
            photo=serialized_bird[7]
        )
