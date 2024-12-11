import hashlib
from http import HTTPStatus
from typing import Optional, Any
from zipfile import ZipFile

from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse

from app.model.Bird import Bird
from app.storage.csv_manager import CSVManager
from app.storage.storage_manager import IStorageManager
from app.util.csv_serializer import CSVSerializer

app = FastAPI()

DATABASE_FILE = "database.csv"
DATABASE_FILE_ZIP = "database.zip"
DATABASE: IStorageManager = CSVManager(DATABASE_FILE, CSVSerializer())

@app.get("/", response_model=list[Bird], status_code=HTTPStatus.OK)
async def get_birds(
    scientific_name: Optional[str] = None,
    common_name: Optional[str] = None,
    location: Optional[str] = None,
    average_size: Optional[float] = None,
    average_weight: Optional[float] = None,
    life_expectancy: Optional[int] = None
) -> list[Any]:
    return DATABASE.get(
        scientific_name,
        common_name,
        location,
        average_size,
        average_weight,
        life_expectancy
    )

@app.get("/count", status_code=HTTPStatus.OK)
async def count_birds() -> dict[str, Any]:
    return {"count_birds": DATABASE.count_birds()}

@app.get("/db-zip", status_code=HTTPStatus.OK)
async def get_database_zip() -> Any:
    with ZipFile(DATABASE_FILE_ZIP, "w") as zip_object:
        zip_object.write(DATABASE_FILE)

    return FileResponse(path=DATABASE_FILE_ZIP, filename="database.zip", media_type="application/zip")

@app.get("/db-hash", status_code=HTTPStatus.OK)
async def get_database_hash() -> dict[str, Any]:
    database_file_bytes = open(DATABASE_FILE, "rb").read()

    return {"hash": hashlib.sha256(database_file_bytes).hexdigest()}

@app.post("/", response_model=Bird, status_code=HTTPStatus.CREATED)
async def create_bird(bird: Bird) -> dict[str, Any]:
    if DATABASE.scientific_name_exists(bird.scientific_name):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"Bird '{bird.scientific_name}' already exists"
        )

    return DATABASE.save(bird).model_dump()

@app.put("/", response_model=Bird, status_code=HTTPStatus.OK)
async def update_bird(old_scientific_name: str, bird: Bird) -> dict[str, Any]:
    try:
        return DATABASE.update(old_scientific_name, bird).model_dump()
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error.args[0])

@app.delete("/", status_code=HTTPStatus.OK)
async def delete_bird(scientific_name: str) -> dict[str, Any]:
    try:
        DATABASE.delete(scientific_name)
        return {"detail": f"{scientific_name} was deleted with success"}
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error.args[0])
