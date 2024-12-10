from http import HTTPStatus
from typing import Optional, Any

from fastapi import FastAPI

from app.model.Bird import Bird
from app.storage.storage_manager import IStorageManager
from app.storage.csv.csv_manager import CSVManager
from app.storage.csv.csv_serializer import CSVSerializer

app = FastAPI()

DATABASE_FILE = "database.csv"
DATABASE: IStorageManager = CSVManager(DATABASE_FILE, CSVSerializer())

@app.post("/", response_model=Bird, status_code=HTTPStatus.CREATED)
async def create_bird(bird: Bird) -> Any:
    return DATABASE.save(bird).model_dump()

@app.get("/", response_model=list[Bird])
async def get_birds(
    scientific_name: Optional[str] = None,
    common_name: Optional[str] = None,
    location: Optional[str] = None,
    average_size: Optional[float] = None,
    average_weight: Optional[float] = None,
    life_expectancy: Optional[int] = None
) -> Any:
    birds = DATABASE.get(
        scientific_name,
        common_name,
        location,
        average_size,
        average_weight,
        life_expectancy
    )

    return birds