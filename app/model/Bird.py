from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Bird(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    scientific_name: str
    common_name: str
    location: str
    average_size: Optional[float] = None
    average_weight: Optional[float] = None
    life_expectancy: Optional[int] = None
    photo: Optional[str] = None
