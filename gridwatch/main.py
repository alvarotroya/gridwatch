from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from gridwatch import database
from gridwatch.crud.exceptions import DatabaseEntityNotFound
from gridwatch.models import customers  # noqa
from gridwatch.routers.connections import router as connections_router
from gridwatch.routers.devices import router as devices_router
from gridwatch.routers.stations import router as stations_router
from gridwatch.routers.transformers import router as transformers_router

app = FastAPI()

SessionDep = Annotated[Session, Depends(database.get_db)]

# NOTE: This should happen with a migration tool like alembic. For now, this suffices
database.create_tables_if_not_existent()

app.include_router(stations_router, tags=["Stations"])
app.include_router(transformers_router, tags=["Transformers"])
app.include_router(connections_router, tags=["Connections"])
app.include_router(devices_router, tags=["Devices"])


# Global error handling for uncatched `DatabaseEntityNotFound` errors -> return 404
@app.exception_handler(DatabaseEntityNotFound)
async def custom_exception_handler(_request, exc: DatabaseEntityNotFound):
    raise HTTPException(
        status_code=404,
        detail=str(exc),
    )


@app.get("/", tags=["Root"])
async def root():
    return {"status": "up"}
