from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from gridwatch import database
from gridwatch.models import customers  # noqa
from gridwatch.routers.stations import router as stations_router

app = FastAPI()

SessionDep = Annotated[Session, Depends(database.get_db)]

# NOTE: This should happen with a migration tool like alembic. For now, this suffices
database.create_tables_if_not_existent()

app.include_router(stations_router, tags=["Stations"])


@app.get("/", tags=["Root"])
async def root():
    return {"status": "up"}
