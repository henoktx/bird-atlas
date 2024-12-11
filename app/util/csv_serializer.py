import csv
from io import StringIO
from typing import Dict

from app.model.Bird import Bird


class CSVSerializer:
    @staticmethod
    def serializer(bird: Bird) -> list[any]:
        return [
                bird.scientific_name,
                bird.common_name,
                bird.location,
                bird.average_size,
                bird.average_weight,
                bird.life_expectancy,
                bird.photo
        ]

    @staticmethod
    def deserializer(serialized_bird: list[any]) -> Bird:
        serialized_bird = [None if value == "" else value for value in serialized_bird]

        return Bird(
            scientific_name=serialized_bird[0],
            common_name=serialized_bird[1],
            location=serialized_bird[2],
            average_size=serialized_bird[3],
            average_weight=serialized_bird[4],
            life_expectancy=serialized_bird[5],
            photo=serialized_bird[6]
        )
