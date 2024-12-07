from typing import Optional

from pydantic import BaseModel

class Bird(BaseModel):
    id: int
    scientific_name: str
    common_name: str
    location: str
    average_size: Optional[float]
    average_weight: Optional[float]
    life_expectancy: Optional[int]
    photo: Optional[str]
