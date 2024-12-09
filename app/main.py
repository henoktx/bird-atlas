from http import HTTPStatus

from fastapi import FastAPI

from app.model.Bird import Bird
from app.storage.storage_manager import IStorageManager
from app.storage.csv.csv_manager import CSVManager
from app.storage.csv.csv_serializer import CSVSerializer

app = FastAPI()

DATABASE_FILE = "database.csv"
DATABASE: IStorageManager = CSVManager(DATABASE_FILE, CSVSerializer())

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/", response_model=Bird, status_code=HTTPStatus.CREATED)
async def create_bird(bird: Bird) -> dict[str, any]:
    return DATABASE.save(bird).model_dump()