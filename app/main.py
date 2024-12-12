import hashlib
import logging
from http import HTTPStatus
from typing import Optional, Any
from zipfile import ZipFile

from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse

from app.model.Bird import Bird
from app.storage.csv_manager import CSVManager
from app.storage.storage_manager import IStorageManager
from app.util.csv_serializer import CSVSerializer

LOG_FILE = "actions.log"

logging.basicConfig(
    filename=LOG_FILE,
    encoding="utf-8",
    level=1,
    filemode="a",
    format="{asctime} {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)

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
    logging.info("Getting birds")

    try:
        birds = DATABASE.get(
            scientific_name,
            common_name,
            location,
            average_size,
            average_weight,
            life_expectancy
        )

        logging.info("Got birds")

        return birds
    except Exception as error:
        logging.error(error.args[0])
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error.args[0])

@app.get("/count", status_code=HTTPStatus.OK)
async def count_birds() -> dict[str, Any]:
    logging.info("Counting birds")

    try:
        birds = DATABASE.count_birds()

        logging.info("Counted birds")

        return {"count_birds": birds}
    except Exception as error:
        logging.error(error.args[0])
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error.args[0])

@app.get("/db-zip", status_code=HTTPStatus.OK)
async def get_database_zip() -> Any:
    logging.info("Downloading database")

    try:
        with ZipFile(DATABASE_FILE_ZIP, "w") as zip_object:
            zip_object.write(DATABASE_FILE)

        logging.info("Downloaded database")

        return FileResponse(path=DATABASE_FILE_ZIP, filename="database.zip", media_type="application/zip")
    except Exception as error:
        logging.error(error.args[0])
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error.args[0])


@app.get("/db-hash", status_code=HTTPStatus.OK)
async def get_database_hash() -> dict[str, Any]:
    logging.info("Generating database file hash")

    try:
        database_file_bytes = open(DATABASE_FILE, "rb").read()

        logging.info("Generating database file hash")

        return {"hash": hashlib.sha256(database_file_bytes).hexdigest()}
    except Exception as error:
        logging.error(error.args[0])
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error.args[0])

@app.post("/", response_model=Bird, status_code=HTTPStatus.CREATED)
async def create_bird(bird: Bird) -> dict[str, Any]:
    logging.info("Creating bird")

    if DATABASE.scientific_name_exists(bird.scientific_name):
        logging.error("Bird already exists")

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"Bird '{bird.scientific_name}' already exists"
        )

    try:
        new_bird = DATABASE.save(bird)

        logging.info("Created bird")

        return new_bird.model_dump()
    except Exception as error:
        logging.error(error.args[0])
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error.args[0])

@app.put("/", response_model=Bird, status_code=HTTPStatus.OK)
async def update_bird(old_scientific_name: str, bird: Bird) -> dict[str, Any]:
    logging.info("Updating bird")

    try:
        updated_bird = DATABASE.update(old_scientific_name, bird)

        logging.info("Updated bird")

        return updated_bird.model_dump()
    except ValueError as error:
        logging.error(error.args[0])
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error.args[0])

@app.delete("/", status_code=HTTPStatus.OK)
async def delete_bird(scientific_name: str) -> dict[str, Any]:
    logging.info("Deleting bird")

    try:
        DATABASE.delete(scientific_name)

        logging.info("Deleted bird")

        return {"detail": f"{scientific_name} was deleted with success"}
    except ValueError as error:
        logging.error(error.args[0])
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error.args[0])
